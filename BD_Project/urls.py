from django.urls import path
from BD import views
#from BD.authorisation import AdminGroup

urlpatterns = [
    path('patients/', views.patient_list, name='patient_list'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('neighborhoods/', views.neighborhood_list, name='neighborhood_list'),
    path('diagnoses/', views.diagnoses_list, name='diagnoses_list'),
    path('visits/', views.visit_list, name='visit_list'),
    path('tickets/', views.ticket_list, name='ticket'),
    path('main/', views.main_view, name='main'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change/', views.change_view, name='change'),
    path('addEmpty/', views.add_empty_row, name='addEmpty'),
    path('get_fields_by_name/', views.get_fields_by_name, name='get_fields_by_name'),
    path('change_by_list/', views.change_by_list, name='change_by_list'),
    path('validate_field/', views.validate_field, name='validate_field'),
    path('row_add/', views.row_add, name='row_add'),
    path('row_delete/', views.row_delete, name='row_delete'),
    path('doc_neigh_doc/',views.doc_neigh_doc, name='doc_neigh_doc')#Вых.док - Вывод списка участков и участковых врачей
]