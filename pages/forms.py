from django import forms

class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(
        label='Upload CV',
        help_text='PDF only',
        widget=forms.FileInput(attrs={'accept': '.pdf'})
    )
    job_offer_text = forms.CharField(
        label='Job Description',
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Paste the job description here'})
    )
    job_title = forms.CharField(  # New field for job title
        label='Job Title',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter the job title'})
    )
    company_name = forms.CharField(  # New field for company name
        label='Company Name',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter the company name'})
    )


class ProfileForm(forms.Form):
    """Form for editing user profile."""
    full_name = forms.CharField(label="Full Name", max_length=255, required=True)
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        required=False
    )
    password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput,
        required=False
    )