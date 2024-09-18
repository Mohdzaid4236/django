# myapp/models.py
from django.db import models

class PersonalInformation(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    alternate_email = models.EmailField(blank=True)
    how_did_you_find_out = models.CharField(max_length=50)
    ready_to_relocate = models.BooleanField()
    address_line_1 = models.CharField(max_length=255,default='Unknown Address')
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100,default='unknown')
    state = models.CharField(max_length=100,default='Unknown')
    zip = models.CharField(max_length=20,default='Unknown')
    country = models.CharField(max_length=100,default='Unknown')
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Address(models.Model):
    personal_info = models.OneToOneField(PersonalInformation, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

class EmploymentHistory(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='employment_history')
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    job_description = models.TextField()

class VisaInformation(models.Model):
    personal_info = models.OneToOneField(PersonalInformation, on_delete=models.CASCADE)
    visa_status = models.CharField(max_length=20, blank=True)
    visa_issue_date = models.DateField(blank=True, null=True)
    visa_expiry_date = models.DateField(blank=True, null=True)
class Qualification(models.Model):
    DEGREE_CHOICES = [
        ('high_school', 'High School'),
        ('associate_degree', 'Associate Degree'),
        ('bachelor_degree', 'Bachelor’s Degree'),
        ('master_degree', 'Master’s Degree'),
    ]

    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='qualifications')
    degree = models.CharField(max_length=50, choices=DEGREE_CHOICES)
    institution = models.CharField(max_length=255)
    year_of_passing = models.PositiveIntegerField()
    additional_certificates = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} from {self.institution} ({self.year_of_passing})"