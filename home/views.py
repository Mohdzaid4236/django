from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.utils.http import int_to_base36
from django.utils.crypto import get_random_string
from .forms import PersonalInformationForm,AddressForm,EmploymentHistoryForm,VisaInformationForm,QualificationForm,CompleteRegistrationForm,CourseSelectionForm,CustomLoginForm,UserRegistrationForm
from .models import PersonalInformation,Address,VisaInformation,EmploymentHistory,Qualification
import uuid
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django import forms
from .models import PersonalInformation, Address, Qualification, EmploymentHistory, VisaInformation
from django.contrib.auth import login,authenticate
@csrf_exempt
@csrf_protect

def index(request):
    return render(request, 'index.html')

def save(self, *args, **kwargs):
    # Custom logic here
    super().save(*args, **kwargs)




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
@csrf_exempt
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('home')  # Change to your home view
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})
@csrf_exempt
def create_account(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('sign_up')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        # Log in the user
        login(request, user)
        
        
        return redirect('register')
    
    return render(request, 'registration/combined_registration.html')
@csrf_exempt
@csrf_protect
def register(request):
    email = request.GET.get('modal_email','')
    print("Captured email:", email)
    if request.method == 'POST':
        personal_info_form = PersonalInformationForm(request.POST,email=email)
        address_form = AddressForm(request.POST)
        visa_info_form = VisaInformationForm(request.POST)
        qualification_form = QualificationForm(request.POST)
        

        # Check the validity of each form
        personal_info_valid = personal_info_form.is_valid()
        address_valid = address_form.is_valid()
        visa_info_valid = visa_info_form.is_valid()
        qualification_valid = qualification_form.is_valid()

        # Save valid forms
        if personal_info_valid:
            personal_info = personal_info_form.save()
        if address_valid:
            address = address_form.save(commit=False)
            if personal_info_valid:  
                address.personal_info = personal_info
            address.save()
        if visa_info_valid:
            visa_info = visa_info_form.save(commit=False)
            if personal_info_valid:
                visa_info.personal_info = personal_info
            visa_info.save()
        if qualification_valid:
            qualifications = qualification_form.save(commit=False)
            if personal_info_valid:
                qualifications.personal_info = personal_info
            qualifications.save()

        # Handle employment histories
        employment_entry_count = request.POST.getlist('employment_0_company_name')  # Getting the first field as a reference
        for i in range(len(employment_entry_count)):  # Iterate through the number of entries
            company_name = request.POST.get(f'employment_{i}_company_name')
            job_title = request.POST.get(f'employment_{i}_job_title')
            start_date = request.POST.get(f'employment_{i}_start_date')
            end_date = request.POST.get(f'employment_{i}_end_date')
            job_description = request.POST.get(f'employment_{i}_job_description')
            currently_working = request.POST.get(f'employment_{i}_currently_working') == 'on'

            if company_name and job_title and start_date and job_description:  # Ensure required fields are filled
                employment = EmploymentHistory(
                    personal_info=personal_info,
                    company_name=company_name,
                    job_title=job_title,
                    start_date=start_date,
                    end_date=end_date,
                    job_description=job_description,
                    currently_working=currently_working
                )
                employment.save()
            else:
                print(f"Invalid employment entry {i}") # Debugging line

        # Optionally, send email notification after everything is saved
        if personal_info_valid:
            send_email_notification(personal_info.email, settings.DEFAULT_FROM_EMAIL, personal_info)

        return render(request, 'registration/success_final.html', {'personal_info': personal_info})
    else:
        personal_info_form = PersonalInformationForm(email=email)
        address_form = AddressForm()
        visa_info_form = VisaInformationForm()
        qualification_form = QualificationForm()
        employment_history_forms = [EmploymentHistoryForm(prefix=f'employment_{i}') for i in range(1)]

    return render(request, 'registration/combined_registration.html', {
        'personal_info_form': personal_info_form,
        'address_form': address_form,
        'visa_info_form': visa_info_form,
        'qualification_form': qualification_form,
        'employment_history_forms': employment_history_forms,
    })


def send_email_notification(user_email, admin_email, personal_info):
    # Create URLs for approval and disapproval
    approval_link = reverse('approve_registration', args=[personal_info.id])
    disapproval_link = reverse('disapprove_registration', args=[personal_info.id])

    # Fetch related models safely
    address = getattr(personal_info, 'address', None)
    qualification = personal_info.qualifications.first() if personal_info.qualifications.exists() else None
    employment_history = personal_info.employment_history.first() if personal_info.employment_history.exists() else None
    visa_info = getattr(personal_info, 'visa_information', None)

    # Email to admin with student information and approval/disapproval links
    admin_subject = 'New Registration Submitted'
    admin_message = f'''
    A new registration has been submitted.

    Student Information:
    Name: {personal_info.first_name} {personal_info.middle_name or ''} {personal_info.last_name}
    Email: {personal_info.email}
    Phone: {personal_info.phone}
    Country Code: {personal_info.country_code}
    Address: {address.address_line_1 if address else 'N/A'}, {address.address_line_2 if address else 'N/A'}, {address.city if address else 'N/A'}, {address.state if address else 'N/A'} {address.postal_code if address else 'N/A'}, {address.country if address else 'N/A'}
    Qualification: {qualification.degree if qualification else 'N/A'}
    Institution: {qualification.institution if qualification else 'N/A'}
    Year of Passing: {qualification.year_of_passing if qualification else 'N/A'}
    Job Title: {employment_history.job_title if employment_history else 'N/A'}
    Company Name: {employment_history.company_name if employment_history else 'N/A'}
    Visa Type: {visa_info.visa_status if visa_info else 'N/A'}

    Please review the registration and decide whether to approve or disapprove:
    Approve: {settings.SITE_URL}{approval_link}
    Disapprove: {settings.SITE_URL}{disapproval_link}
    '''
    send_mail(admin_subject, admin_message, settings.EMAIL_HOST_USER, [admin_email])

    # Email to user with a thank you message
    user_subject = 'Thank You for Your Registration'
    user_message = f'''
    Dear {personal_info.first_name},

    Thank you for registering with us. We have received your registration and will review it shortly.

    You will receive further instructions once your registration has been processed.

    Best regards,
    Binary Academy
    '''
    send_mail(user_subject, user_message, settings.EMAIL_HOST_USER, [user_email])

def approve_registration(request, registration_id):
    registration = get_object_or_404(PersonalInformation, id=registration_id)
    # Mark the registration as approved
    registration.is_approved = True
    registration.save()
    course_selection_link = reverse('course_selection', args=[registration_id])
    course_selection_url = f"{settings.SITE_URL}{course_selection_link}"

    # Send confirmation email to the user
    send_mail(
        'Registration Approved',
        f'''
        Congratulations! Your registration has been approved.

        Please select your courses and payment method using the following link:
        {course_selection_url}

        Best regards,
        Binary Academy
        ''',
        settings.DEFAULT_FROM_EMAIL,
        [registration.email],
        fail_silently=False,
    )

    return redirect('index')

def disapprove_registration(request, registration_id):
    registration = get_object_or_404(PersonalInformation, id=registration_id)
    # Mark the registration as disapproved
    registration.is_approved = False
    registration.save()

    # Send email to the user
    send_mail(
        'Registration Disapproved',
        'Sorry, your registration has been disapproved.',
        settings.DEFAULT_FROM_EMAIL,
        [registration.email],
        fail_silently=False,
    )

    return redirect('index')

def course_selection(request, registration_id):
    personal_info = get_object_or_404(PersonalInformation, id=registration_id)

    if request.method == 'POST':
        form = CourseSelectionForm(request.POST)
        if form.is_valid():
            selected_courses = form.cleaned_data['selected_courses']
            personal_info.selected_courses.set(selected_courses)
            personal_info.save()

            messages.success(request, "Courses selected successfully.")
            return redirect('payment')
    else:
        form = CourseSelectionForm()

    return render(request, 'registration/course_selection.html', {
        'form': form,
    })



def success(request):
    return render(request, 'registration/success.html')