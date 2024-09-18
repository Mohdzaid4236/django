# myapp/forms.py
from django import forms
from .models import PersonalInformation, Address, EmploymentHistory, VisaInformation,Qualification

class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = [
            'first_name', 'middle_name', 'last_name', 'country_code', 'phone',
            'email', 'alternate_email', 'how_did_you_find_out', 'ready_to_relocate'
        ]

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'postal_code']
class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['degree', 'institution', 'year_of_passing']

class EmploymentHistoryForm(forms.ModelForm):
    class Meta:
        model = EmploymentHistory
        fields = ['company_name', 'job_title', 'start_date', 'end_date', 'job_description']

class VisaInformationForm(forms.ModelForm):
    class Meta:
        model = VisaInformation
        fields = ['visa_status', 'visa_issue_date', 'visa_expiry_date']

class CompleteRegistrationForm(forms.Form):
    personal_info = PersonalInformationForm()
    address = AddressForm()
    employment_history = forms.ModelMultipleChoiceField(queryset=EmploymentHistory.objects.none(), required=False)
    qualification=QualificationForm()
    visa_info = VisaInformationForm()
