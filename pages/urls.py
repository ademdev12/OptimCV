from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from . import views


# --- URL Patterns ---
urlpatterns = [
    # Public Views
    path('', views.home, name='home'),

    # Authentication Views
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('forgot-password/', views.ForgotPassword, name='forgot_password'),
    path('reset-password/', views.ResetPasswordConfirm, name='reset_password_confirm'),
    path('reset-password-complete/', views.ResetPasswordComplete, name='reset_password_complete'),
    path('logout/', views.logout_view, name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),

    # Dashboard and Subscription Views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upgrade-plan/', views.upgrade_plan, name='upgrade_plan'),
    path('payment_success/', views.payment_success, name='payment_success'),

    # Profile Views
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Resume Optimization Views
    path('upload_cv/', views.upload_cv, name='upload_cv'),
    path('result/<int:optimization_id>/', views.optimization_result, name='optimization_result'),
    path('history/', views.optimization_history, name='optimization_history'),
]

# --- Static Media Configuration ---
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)