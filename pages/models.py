from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class UserSubscription(models.Model):
    """
    Model to manage user subscriptions.
    Each user can have only one subscription at a time (One-to-One relationship with the User model).
    """
    # Fields
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(
        max_length=20,
        choices=[('Free', 'Free'), ('Premium', 'Premium')],
        default='Free'
    )
    subscription_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    # Methods
    def save(self, *args, **kwargs):
        """
        Override the save method to set subscription dates for Premium plans.
        """
        if self.plan == 'Premium':
            self.subscription_date = timezone.now()
            self.expiration_date = self.subscription_date + timedelta(days=30)
        elif self.plan == 'Free':
            self.expiration_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.plan} plan"


class Payment(models.Model):
    """
    Model to store information about payments made by users.
    A payment is associated with a specific user and a Stripe payment intent.
    """
    # Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_payment_intent = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    currency = models.CharField(max_length=10, default='usd')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')

    # Methods
    def __str__(self):
        return f"{self.user.email} - {self.amount} {self.currency} ({self.status})"


class ResumeOptimization(models.Model):
    
    """
    Model to handle resume optimization data based on job offers.
    Stores original and optimized resumes along with analysis results.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes/')
    job_offer_text = models.TextField()
    match_score = models.FloatField()
    suggestions = models.TextField()
    plan_used = models.CharField(max_length=20, choices=[('Free', 'Free'), ('Premium', 'Premium')])
    optimized_resume_1 = models.FileField(upload_to='optimized_resumes/', null=True, blank=True)
    optimized_resume_1_docx = models.FileField(upload_to='optimized_resumes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)  # New field
    company_name = models.CharField(max_length=100, null=True, blank=True)  # New field

    def __str__(self):
        return f"Optimization {self.id} by {self.user.username}"
    

