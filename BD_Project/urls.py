from django.urls import path
from BD import views

urlpatterns = [
    path('patients/', views.patient_list, name='patient_list'),
]