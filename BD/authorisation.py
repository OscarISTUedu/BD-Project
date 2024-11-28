from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from BD.models import Doctor, Patient, Ticket, Diagnosis, Neighborhood, Visit

DoctorGroup,flag = Group.objects.get_or_create(name='Врачи')
PatientGroup,flag = Group.objects.get_or_create(name='Пациенты')
AdminGroup,flag = Group.objects.get_or_create(name='Администрация')
ReceptionGroup,flag = Group.objects.get_or_create(name='Регистратура')
#Доктор
'''
Просмотр - Врачи,Пациенты,Талон,Диагнозы
Изменение - Талон
Удаление
Добавление

'''
doctor_content_type = ContentType.objects.get_for_model(Doctor)
patient_content_type = ContentType.objects.get_for_model(Patient)
ticket_content_type = ContentType.objects.get_for_model(Ticket)
diagnosis_content_type = ContentType.objects.get_for_model(Diagnosis)
neighborhood_content_type = ContentType.objects.get_for_model(Neighborhood)
visit_content_type = ContentType.objects.get_for_model(Visit)

view_doctor_permission = Permission.objects.get_or_create(
    codename='view_doctor',
    name='Can view doctor',
    content_type=doctor_content_type,)
view_patient_permission = Permission.objects.get_or_create(
    codename='view_patient',
    name='Can view patient',
    content_type=patient_content_type,)
view_ticket_permission = Permission.objects.get_or_create(
    codename='view_ticket',
    name='Can view ticket',
    content_type=ticket_content_type,)
view_diagnosis_permission = Permission.objects.get_or_create(
    codename='view_diagnosis',
    name='Can view diagnosis',
    content_type=diagnosis_content_type,)
change_ticket_permission = Permission.objects.get_or_create(
    codename='change_ticket',
    name='Can change tickets',
    content_type=ticket_content_type,)
doctor_permission = Permission.objects.filter(codename__in=['view_doctor', 'view_patient','view_ticket','view_diagnosis','change_ticket'])
DoctorGroup.permissions.set(doctor_permission)
DoctorGroup.refresh_from_db()
first = User.objects.filter(username='doctor_A')[0]
first.groups.add(DoctorGroup)
