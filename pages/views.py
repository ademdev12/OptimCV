from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import UserSubscription, Payment, ResumeOptimization
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import stripe
from django.urls import reverse
from .forms import ResumeUploadForm, ProfileForm
from .utils import validate_password, extract_text_from_pdf, calculate_match_score, generate_suggestions, analyze_cv_structure , optimize_cv
from .file_utils import  create_pdf_from_docx , create_docx
from .constants import PREMIUM_PLAN_PRICE, PREMIUM_PLAN_NAME, CURRENCY, FREE_OPTIMIZATION_LIMIT
import time
from django.db.models import Avg
from datetime import datetime
import re
from django.core.files.base import ContentFile
import logging
logger = logging.getLogger(__name__)


# --- Authentication Views ---

def login_view(request):
    """Handle user login and redirect to dashboard on success."""
    if request.method == "POST":
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '').strip()

        if not email or not password:
            messages.error(request, "All fields are required.")
            return redirect('login')

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            subscription = UserSubscription.objects.filter(user=user).first()
            if not subscription:
                UserSubscription.objects.create(user=user, plan='Free')
            return redirect('dashboard')
        messages.error(request, "Invalid email or password.")

    return render(request, 'pages/login.html')


def signup(request):
    """Handle user signup with validation and create a free subscription."""
    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        if not full_name or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('signup')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already in use.")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        password_error = validate_password(password1)
        if password_error:
            messages.error(request, password_error)
            return redirect('signup')

        user = User.objects.create_user(username=email, email=email, password=password1)
        user.first_name = full_name
        user.save()
        UserSubscription.objects.create(user=user, plan='Free')
        messages.success(request, "🎉 Account successfully created!")
        return redirect('login')

    return render(request, 'pages/signup.html')


def logout_view(request):
    """Log out the user and redirect to login page."""
    logout(request)
    return redirect('login')


# --- Subscription Management Views ---

@login_required
def dashboard(request):
    subscription = UserSubscription.objects.filter(user=request.user).first()
    plan = subscription.plan if subscription else "Free"
    optimizations = ResumeOptimization.objects.filter(user=request.user)
    optimization_count = optimizations.count()
    average_score = optimizations.aggregate(avg_score=Avg('match_score'))['avg_score']
    plan_progress = min((optimization_count / FREE_OPTIMIZATION_LIMIT) * 100, 100) if plan == "Free" else 100
    latest_optimization = optimizations.order_by('-created_at').first()
    recent_optimizations = optimizations.order_by('-created_at')[:5]

    # Pour Free : Combien d’optimisations restantes
    optimizations_remaining = max(FREE_OPTIMIZATION_LIMIT - optimization_count, 0) if plan == "Free" else 0

    # Pour Premium : Combien de jours restants
    subscription_days_remaining = None
    if plan == "Premium" and subscription:
        end_date = subscription.expiration_date  # Suppose un champ `end_date` dans ton modèle
        if end_date:
            subscription_days_remaining = (end_date.date() - datetime.now().date()).days
            subscription_days_remaining = max(subscription_days_remaining, 0)

    context = {
        'plan': plan,
        'optimization_count': optimization_count,
        'average_score': average_score,
        'plan_progress': plan_progress,
        'latest_optimization': latest_optimization,
        'recent_optimizations': recent_optimizations,
        'optimizations_remaining': optimizations_remaining,
        'subscription_days_remaining': subscription_days_remaining,
        'FREE_OPTIMIZATION_LIMIT': FREE_OPTIMIZATION_LIMIT,  # Par exemple, 5
    }
    return render(request, 'pages/dashboard.html', context)


@login_required
def upgrade_plan(request):
    """Handle upgrading the user's plan to Premium via Stripe."""
    subscription = UserSubscription.objects.filter(user=request.user).first()
    if not subscription:
        return redirect('dashboard')

    if subscription.plan == 'Premium':
        messages.info(request, "You are already on the Premium plan.")
        return redirect('dashboard')

    if request.method == "POST":
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': CURRENCY,
                        'product_data': {'name': PREMIUM_PLAN_NAME},
                        'unit_amount': PREMIUM_PLAN_PRICE,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri('/upgrade/'),
                customer_email=request.user.email,
            )
            return redirect(session.url, code=303)
        except stripe.error.StripeError as e:
            messages.error(request, f"An error occurred: {e.user_message}")
            return redirect('upgrade_plan')

    return render(request, 'pages/upgrade_plan.html', {'subscription': subscription})


@login_required
def payment_success(request):
    """Process successful payment and upgrade user to Premium."""
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "Stripe session not found.")
        return redirect('dashboard')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        payment_intent = session.payment_intent
        amount_total = session.amount_total / 100
        currency = session.currency
    except Exception as e:
        messages.error(request, f"Stripe Error: {getattr(e, 'user_message', str(e))}")
        return redirect('dashboard')

    if not Payment.objects.filter(stripe_payment_intent=payment_intent).exists():
        Payment.objects.create(
            user=request.user,
            stripe_payment_intent=payment_intent,
            amount=amount_total,
            currency=currency,
            status='succeeded'
        )
        subscription = UserSubscription.objects.filter(user=request.user).first()
        if subscription:
            subscription.plan = 'Premium'
            subscription.subscription_date = timezone.now()
            subscription.expiration_date = None
            subscription.save()
        messages.success(request, "🎉 Payment successful! You are now Premium.")

    return redirect('dashboard')


# --- Password Management Views ---

def ForgotPassword(request):
    """Handle password reset request by email."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        if not email:
            messages.error(request, "Email is required.")
            return redirect('forgot_password')

        user = User.objects.filter(email=email).first()
        if user:
            request.session['reset_email'] = email
            return redirect('reset_password_confirm')
        messages.error(request, 'Email not found.')

    return render(request, 'pages/ForgotPassword.html')


def ResetPasswordConfirm(request):
    """Confirm and update new password for reset."""
    email = request.session.get('reset_email', None)
    if not email:
        return redirect('forgot_password')

    if request.method == 'POST':
        password1 = request.POST.get('new_password1', '').strip()
        password2 = request.POST.get('new_password2', '').strip()

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password_confirm')

        password_error = validate_password(password1)
        if password_error:
            messages.error(request, password_error)
            return redirect('reset_password_confirm')

        user = User.objects.filter(email=email).first()
        if user:
            user.set_password(password1)
            user.save()
            del request.session['reset_email']
            return redirect('reset_password_complete')
        messages.error(request, 'User not found.')

    return render(request, 'pages/reset_password_confirm.html')


def ResetPasswordComplete(request):
    """Display password reset completion page."""
    return render(request, 'pages/reset_password_complete.html')


# --- Main Views ---

def home(request):
    """Render the homepage."""
    return render(request, 'pages/home.html')


@login_required
def profile_view(request):
    """Display user profile information."""
    user = request.user
    subscription = UserSubscription.objects.filter(user=user).first()
    plan = subscription.plan if subscription else "Free"
    context = {
        'full_name': user.first_name,
        'email': user.email,
        'plan': plan,
    }
    return render(request, 'pages/profile.html', context)


@login_required
def edit_profile(request):
    """Handle profile updates including name and password."""
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['full_name']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1:
                if password1 != password2:
                    messages.error(request, "Passwords do not match.")
                    return redirect('edit_profile')
                user.set_password(password1)
                update_session_auth_hash(request, user)

            user.save()
            
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_view')
    else:
        form = ProfileForm(initial={'full_name': user.first_name})

    context = {'form': form, 'email': user.email}
    return render(request, 'pages/edit_profile.html', context)


@login_required
def upload_cv(request):
    """Handle CV upload and optimization using the new analysis and optimization functions."""
    subscription = UserSubscription.objects.filter(user=request.user).first()
    plan = subscription.plan if subscription else "Free"
    optimization_count = ResumeOptimization.objects.filter(user=request.user).count()
    optimizations_remaining = FREE_OPTIMIZATION_LIMIT - optimization_count if plan == "Free" else None

    if plan == "Free" and optimization_count >= FREE_OPTIMIZATION_LIMIT:
        messages.error(request, "You have reached the limit of free optimizations. Upgrade to Premium!")
        return redirect('dashboard')

    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = form.cleaned_data['resume_file']
            job_offer_text = form.cleaned_data['job_offer_text']
            job_title = form.cleaned_data['job_title']
            company_name = form.cleaned_data['company_name']

            # Validate file type
            if not resume_file.name.lower().endswith('.pdf'):
                messages.error(request, "Please upload a PDF file.")
                return redirect('upload_cv')

            try:
                # Extract text and analyze CV structure
                resume_text = extract_text_from_pdf(resume_file)
                if not resume_text.strip():
                    messages.error(request, "Could not extract text from the PDF. Please try another file.")
                    return redirect('upload_cv')

                cv_analysis = analyze_cv_structure(resume_text)
                
                # Calculate match score
                match_score = calculate_match_score(resume_text, job_offer_text, plan)
                time.sleep(2)  # Rate limiting

                # Generate suggestions
                suggestions_text = generate_suggestions(resume_text, job_offer_text, plan)
                time.sleep(2)
                
                suggestions_list = [
                    line.strip()[2:].replace('**', '') 
                    for line in suggestions_text.split('\n') 
                    if line.strip().startswith('- ') and line.strip()[2:]
                ]

                # Generate optimized CV using the new function
                optimized_cv = optimize_cv(resume_text, job_offer_text, cv_analysis)
                time.sleep(2)

                # Create optimization record
                optimization = ResumeOptimization(
                    user=request.user,
                    resume_file=resume_file,
                    job_offer_text=job_offer_text,
                    match_score=match_score,
                    suggestions=suggestions_text,
                    plan_used=plan,
                    job_title=job_title,
                    company_name=company_name
                )

                # Generate PDF
                pdf_buffer = create_pdf_from_docx(create_docx(optimized_cv))
                if not pdf_buffer:
                    raise Exception("PDF generation failed")

                optimization.optimized_resume_1.save(
                    f"optimized_{resume_file.name.rsplit('.', 1)[0]}.pdf",
                    ContentFile(pdf_buffer.getvalue())
                )

                # Generate DOCX for Premium users
                if plan == "Premium":
                    docx_buffer = create_docx(optimized_cv)
                    optimization.optimized_resume_1_docx.save(
                        f"optimized_{resume_file.name.rsplit('.', 1)[0]}.docx",
                        ContentFile(docx_buffer.getvalue())
                    )

                optimization.save()
                messages.success(request, "Your CV has been successfully optimized!")
                return render(request, 'pages/optimization_result.html', {
                    'form': form,
                    'plan': plan,
                    'optimization': optimization,
                    'suggestions_list': suggestions_list,
                    'optimizations_remaining': optimizations_remaining
                })

            except Exception as e:
                logger.error(f"CV optimization error: {str(e)}", exc_info=True)
                messages.error(request, f"An error occurred during optimization: {str(e)}")
                return redirect('upload_cv')

    else:
        form = ResumeUploadForm()

    return render(request, 'pages/upload_cv.html', {
        'form': form,
        'plan': plan,
        'optimization_count': optimization_count,
        'optimizations_remaining': optimizations_remaining
    })
@login_required
def optimization_result(request, optimization_id):
    """Display the optimization result for a specific resume."""
    optimization = get_object_or_404(ResumeOptimization, id=optimization_id, user=request.user)
    
    # Pré-formater les suggestions en liste et retirer les ** si présents
    suggestions_list = [
        line.strip()[2:].replace('**', '') for line in optimization.suggestions.split('\n')
        if line.strip().startswith('- ')
    ]
    
    context = {
        'optimization': optimization,
        'suggestions_list': suggestions_list,
        'plan': optimization.plan_used
    }
    return render(request, 'pages/optimization_result.html', context)


@login_required
def optimization_history(request):
    """Display the user's optimization history based on their plan."""
    subscription = UserSubscription.objects.filter(user=request.user).first()
    plan = subscription.plan if subscription else "Free"

    if plan == "Free":
        optimizations = ResumeOptimization.objects.filter(user=request.user).order_by('-created_at')
    else:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        optimizations = ResumeOptimization.objects.filter(
            user=request.user,
            created_at__gte=thirty_days_ago
        ).order_by('-created_at')

    # Pré-formater les suggestions pour chaque optimisation et retirer les ** si présents
    for opt in optimizations:
        opt.suggestions_list = [
            line.strip()[2:].replace('**', '') for line in opt.suggestions.split('\n')
            if line.strip().startswith('- ')
        ]

    optimizations_remaining = (10 - optimizations.count()) if plan == "Free" else None

    context = {
        'optimizations': optimizations,
        'plan': plan,
        'optimizations_remaining': optimizations_remaining
    }
    return render(request, 'pages/optimization_history.html', context)