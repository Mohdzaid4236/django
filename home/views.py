from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.utils.http import int_to_base36
from django.utils.crypto import get_random_string
from .forms import PersonalInformationForm,AddressForm,EmploymentHistoryForm,VisaInformationForm,QualificationForm,CompleteRegistrationForm
from .models import PersonalInformation,Address,VisaInformation,EmploymentHistory,Qualification
import uuid

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'home/about.html')

def services(request):
    return render(request, 'home/index.html')

def contact(request):
    return render(request, 'home/about.html')

def campus(request):
    return render(request, 'home/about.html')

def policy(request):
    return render(request, 'home/about.html')

def student(request):
    return render(request, 'home/about.html')
#def send_email_notification(user_email, admin_email, registration):
    # Create URLs for approval and disapproval
    approval_link = reverse('approve_registration', args=[registration.id])
    disapproval_link = reverse('disapprove_registration', args=[registration.id])
    
    # Email to admin with student information and approval/disapproval links
    admin_subject = 'New Registration Submitted'
    admin_message = f'''
    A new registration has been submitted.

    Student Information:
    Name: {registration.first_name} {registration.middle_name} {registration.last_name}
    Email: {registration.email}
    Phone: {registration.phone}
    Country Code: {registration.country_code}
    Address: {registration.address_line_1}, {registration.address_line_2}, {registration.city}, {registration.state} {registration.zip}, {registration.country}
    Qualification: {registration.qualification_name}
    Institution: {registration.institution}
    Year of Passing: {registration.year_of_passing}
    Job Title: {registration.job_title}
    Company Name: {registration.company_name}
    Visa Type: {registration.visa_type}

    Please review the registration and decide whether to approve or disapprove:
    Approve: {settings.SITE_URL}{approval_link}
    Disapprove: {settings.SITE_URL}{disapproval_link}
    '''
    send_mail(admin_subject, admin_message, settings.EMAIL_HOST_USER, [admin_email])

    # Email to user with a thank you message
    user_subject = 'Thank You for Your Registration'
    user_message = f'''
    Dear {registration.first_name},

    Thank you for registering with us. We have received your registration and will review it shortly.

    You will receive further instructions once your registration has been processed.

    Best regards,
    Binary Academy
    '''
    send_mail(user_subject, user_message, settings.EMAIL_HOST_USER, [user_email])

def register(request):
    if request.method == 'POST':
        personal_info_form = PersonalInformationForm(request.POST)
        address_form = AddressForm(request.POST)
        visa_info_form = VisaInformationForm(request.POST)
        qualification_form=QualificationForm(request.POST)
        employment_history_forms = []
        
        if (personal_info_form.is_valid() and address_form.is_valid() and visa_info_form.is_valid() and qualification_form.is_valid()):
            personal_info = personal_info_form.save()
            address = address_form.save(commit=False)
            address.personal_info = personal_info
            address.save()

            visa_info = visa_info_form.save(commit=False)
            visa_info.personal_info = personal_info
            visa_info.save()

            qualification = qualification_form.save(commit=False)
            qualification.personal_info = personal_info
            qualification.save()

            employment_histories = request.POST.getlist('employment_history')
            for i, history_id in enumerate(employment_histories):
                history_form = EmploymentHistoryForm(request.POST, prefix=f'employment_{i}')
                if history_form.is_valid():
                    employment = history_form.save(commit=False)
                    employment.personal_info = personal_info
                    employment.save()
            send_email_notification(personal_info.email, settings.DEFAULT_FROM_EMAIL, personal_info)

            return redirect('success')
    else:
        personal_info_form = PersonalInformationForm()
        address_form = AddressForm()
        visa_info_form = VisaInformationForm()
        qualification_form=QualificationForm()
        employment_history_forms = [EmploymentHistoryForm(prefix=f'employment_{i}') for i in range(1)]  # Initial formset

    return render(request, 'registration/combined_registration.html', {
        'personal_info_form': personal_info_form,
        'address_form': address_form,
        'visa_info_form': visa_info_form,
        'qualification_form':qualification_form,
        'employment_history_forms': employment_history_forms,
    })

#def approve_registration(request, registration_id):
    registration = get_object_or_404(CompleteRegistrationForm, id=registration_id)
    # Mark the registration as approved
    registration.is_approved = True  # Add a field to the model for this status if needed
    registration.save()

    # Send confirmation email to the user
    send_mail(
        'Registration Approved',
        'Congratulations! Your registration has been approved.',
        settings.DEFAULT_FROM_EMAIL,
        [registration.email],
        fail_silently=False,
    )

    return redirect('admin:home_registration_changelist')  # Redirect to the admin list view or wherever appropriate

#def disapprove_registration(request, registration_id):
    registration = get_object_or_404(CompleteRegistrationForm, id=registration_id)
    # Mark the registration as disapproved
    registration.is_approved = False  # Add a field to the model for this status if needed
    registration.save()

    # Send email to the user
    send_mail(
        'Registration Disapproved',
        'Sorry, your registration has been disapproved.',
        settings.DEFAULT_FROM_EMAIL,
        [registration.email],
        fail_silently=False,
    )

    return redirect('admin:home_registration_changelist')
def send_email_notification(user_email, admin_email, registration,personal_info):
    qualifications = personal_info.qualifications.all() 
    qualifications_info = "\n".join([
        f"Degree: {qual.degree}, Institution: {qual.institution}, Year of Passing: {qual.year_of_passing}"
        for qual in qualifications
    ])
    # Create URLs for approval and disapproval
    #address = Address.objects.filter(personal_info=personal_info).first()
    #approval_link = reverse('approve_registration', args=[registration.id])
    #disapproval_link = reverse('disapprove_registration', args=[registration.id])
    
    # Email to admin with student information and approval/disapproval links
    admin_subject = 'New Registration Submitted'
    admin_message = f'''
    A new registration has been submitted.

    Student Information:
    Name: {registration.first_name} {registration.middle_name} {registration.last_name}
    Email: {registration.email}
    Phone: {registration.phone}
    Country Code: {registration.country_code}
    Address: {registration.address_line_1}, {registration.address_line_2}, {registration.city}, {registration.state} {registration.zip}, {registration.country}
    Qualification: {registration.qualifications}
    Institution: {registration.Institution}
    Year of Passing: {registration.year_of_passing}
    Job Title: {registration.job_title}
    Company Name: {registration.company_name}
    Visa Type: {registration.visa_type}

    Please review the registration and decide whether to approve or disapprove:

    '''
    send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [admin_email])

    # Email to user with a thank you message
    user_subject = 'Thank You for Your Registration'
    user_message = f'''
    Dear {registration.first_name},

    Thank you for registering with us. We have received your registration and will review it shortly.

    You will receive further instructions once your registration has been processed.

    Best regards,
    Binary Academy
    '''
    send_mail(user_subject, user_message, settings.DEFAULT_FROM_EMAIL, [user_email])


def success(request):
    return render(request, 'registration/success.html')
