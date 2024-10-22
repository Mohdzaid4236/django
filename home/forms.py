from django import forms
from django.contrib.auth.models import User
from .models import PersonalInformation, Address, EmploymentHistory, VisaInformation, Qualification, Course
from django.contrib.auth.forms import AuthenticationForm

# User Registration Form
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

# Personal Information Form
class PersonalInformationForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = PersonalInformation
        fields = [
            'first_name', 'middle_name', 'last_name', 'country_code', 'phone',
            'email', 'alternate_email', 'how_did_you_find_out', 'ready_to_relocate'
        ]

    def __init__(self, *args, **kwargs):
        email = kwargs.pop('email', None)  # Pop email if provided in kwargs
        super().__init__(*args, **kwargs)
        if email:
            self.fields['email'].initial = email

# Address Form
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country']

# Qualification Form
class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['degree', 'institution', 'year_of_passing', 'additional_certificates']

# Employment History Form
class EmploymentHistoryForm(forms.ModelForm):
    class Meta:
        model = EmploymentHistory
        fields = ['company_name', 'job_title', 'start_date', 'end_date', 'job_description']

# Visa Information Form
class VisaInformationForm(forms.ModelForm):
    class Meta:
        model = VisaInformation
        fields = ['visa_status', 'visa_issue_date', 'visa_expiry_date']

# Complete Registration Form
class CompleteRegistrationForm(forms.Form):
    personal_info = PersonalInformationForm()
    address = AddressForm()
    employment_history = forms.ModelMultipleChoiceField(queryset=EmploymentHistory.objects.none(), required=False)
    qualification = QualificationForm()
    visa_info = VisaInformationForm()

    def __init__(self, *args, **kwargs):
        email = kwargs.pop('email', None)  # Pop email if available
        super().__init__(*args, **kwargs)

        # Initialize PersonalInformationForm with email if provided
        self.fields['personal_info'] = PersonalInformationForm(email=email) if email else PersonalInformationForm()

        # Dynamically set queryset for employment history, you can filter based on user/context
        self.fields['employment_history'].queryset = EmploymentHistory.objects.all()

# Course Selection Form
class CourseSelectionForm(forms.Form):
    selected_courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Courses"
    )

# Custom Login Form
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
