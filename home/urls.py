from django.contrib import admin
from django.urls import path
from . import views  # Import your views module
#  from .views import approve_registration,disapprove_registration
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Home page
    path('about/', views.about, name='about'),  # About page
    path('services/', views.services, name='services'),  # Services page
    path('contact/', views.contact, name='contact'),  # Contact page
    path('campus/', views.campus, name='campus'),  # Campus page
    path('policy/', views.policy, name='policy'),  # Policy page
    path('students/', views.student, name='students'),  # Students page
    path('register/', views.register, name='register'), #Register page
   # path('approve/<int:registration_id>/', approve_registration, name='approve_registration'),
    #path('disapprove/<int:registration_id>/', disapprove_registration, name='disapprove_registration'),
    path('success/',views.success,name='success')#success page
]
