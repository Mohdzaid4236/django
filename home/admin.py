# myapp/admin.py
from django.contrib import admin
from .models import PersonalInformation, Address, EmploymentHistory, VisaInformation,Qualification

class AddressInline(admin.StackedInline):
    model = Address

class VisaInformationInline(admin.StackedInline):
    model = VisaInformation

class EmploymentHistoryInline(admin.TabularInline):
    model = EmploymentHistory

class QualificationInline(admin.TabularInline):
    model = Qualification
    

class PersonalInformationAdmin(admin.ModelAdmin):
    inlines = [AddressInline, VisaInformationInline, EmploymentHistoryInline,QualificationInline]



admin.site.register(PersonalInformation, PersonalInformationAdmin)
admin.site.register(Address)
admin.site.register(EmploymentHistory)
admin.site.register(VisaInformation)
admin.site.register(Qualification)