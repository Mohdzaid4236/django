from django.contrib import admin
from .models import PersonalInformation, Address, Qualification, EmploymentHistory, VisaInformation

@admin.register(PersonalInformation)
class PersonalInformationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('personal_info', 'city', 'state', 'postal_code', 'country')

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('personal_info', 'degree', 'institution', 'year_of_passing')

@admin.register(EmploymentHistory)
class EmploymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('personal_info', 'company_name', 'job_title', 'start_date', 'end_date')

@admin.register(VisaInformation)
class VisaInformationAdmin(admin.ModelAdmin):
    list_display = ('personal_info', 'visa_status', 'visa_issue_date', 'visa_expiry_date')
