from django.db import models
import uuid
from django.utils import timezone

class PersonalInformation(models.Model):

    HOW_DID_YOU_FIND_OUT_CHOICES = [
        ('counseller', 'Academic Counseller'),
        ('friend', 'Friend'),
        ('advertisement', 'Advertisement'),
    ]
    
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True,null=True)
    last_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    alternate_email = models.EmailField(blank=True,null=True)
    how_did_you_find_out = models.CharField(max_length=50, choices=HOW_DID_YOU_FIND_OUT_CHOICES)
    ready_to_relocate = models.BooleanField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Address(models.Model):
    personal_info = models.OneToOneField(PersonalInformation, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True,null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

class Qualification(models.Model):
    DEGREE_CHOICES = [
        ('high_school', 'High School'),
        ('associate', 'Associate'),
        ('bachelor', 'Bachelor\'s'),
        ('master', 'Master\'s'),
    ]
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='qualifications')
    degree = models.CharField(max_length=50, choices=DEGREE_CHOICES)
    institution = models.CharField(max_length=255)
    year_of_passing = models.PositiveIntegerField()
    additional_certificates = models.CharField(max_length=100, blank=True,null=True)

    def __str__(self):
        return f"{self.degree} from {self.institution} ({self.year_of_passing})"

class EmploymentHistory(models.Model):
    personal_info = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, related_name='employment_history')
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    job_description = models.TextField()
    currently_working = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Employment History"
        verbose_name_plural = "Employment Histories"

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class VisaInformation(models.Model):
    personal_info = models.OneToOneField(PersonalInformation, on_delete=models.CASCADE)
    visa_status = models.CharField(max_length=20)
    visa_issue_date = models.DateField(default=timezone.now)
    visa_expiry_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Visa Status: {self.visa_status} for {self.personal_info}"

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
