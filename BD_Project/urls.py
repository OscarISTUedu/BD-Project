from django.urls import path
from BD import views

urlpatterns = [
    path('patients/', views.patient_list, name='patient_list'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('neighborhoods/', views.neighborhood_list, name='neighborhood_list'),
    path('diagnoses/', views.diagnoses_list, name='diagnoses_list'),
    path('visits/', views.visit_list, name='visit_list'),
    path('tickets/', views.ticket, name='ticket'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]