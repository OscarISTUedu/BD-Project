from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from BD.models import Doctor, Patient, Ticket, Diagnosis, Neighborhood, Visit

def group_required(group_name):#Если пользователь есть хоть в 1 группе - True
    def in_group(user):
        for group in group_name:
            if user.groups.filter(name=group).exists() or user.is_superuser:
                return True
    return user_passes_test(in_group)

DoctorGroup,flag = Group.objects.get_or_create(name='Врачи')
PatientGroup,flag = Group.objects.get_or_create(name='Пациенты')
AdminGroup,flag = Group.objects.get_or_create(name='Администрация')
ReceptionGroup,flag = Group.objects.get_or_create(name='Регистратура')
#Врачи
'''
Просмотр - Врачи,Пациенты,Талон,Диагнозы
Изменение - Талон
'''
#Пациенты
'''
Просмотр - Врачи,Участки
Вых.док - Вывод списка участков и участковых врачей
'''
#Регистратура
'''
Просмотр - Талон,Участки,Пациенты
Изменение - Талон,Участки
Удаление - Талон,Участки
Добавление - Талон,Участки
Вых.док - Вывод талонов
'''
#Администратор
'''
Просмотр - Врачи,Талон,Участки,Пациенты,Диагнозы,Цели
Изменение - Врачи,Талон,Участки,Пациенты,Диагнозы,Цели
Удаление - Врачи,Талон,Участки,Пациенты,Диагнозы,Цели
Добавление - Врачи,Талон,Участки,Пациенты,Диагнозы,Цели
Вых.док - Вывод списка пациентов с определённым диагнозом
Вых.док - Вывод списка участков и участковых врачей
Вых.док - Вывод списка пациентов побывавших на приеме у определенного врача за определенный период
'''
doctor_content_type = ContentType.objects.get_for_model(Doctor)
patient_content_type = ContentType.objects.get_for_model(Patient)
ticket_content_type = ContentType.objects.get_for_model(Ticket)
diagnosis_content_type = ContentType.objects.get_for_model(Diagnosis)
neighborhood_content_type = ContentType.objects.get_for_model(Neighborhood)
visit_content_type = ContentType.objects.get_for_model(Visit)

#Чтение

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
view_neighborhood_permission = Permission.objects.get_or_create(
    codename='view_neighborhood',
    name='Can view neighborhood',
    content_type=neighborhood_content_type,)
view_visit_permission = Permission.objects.get_or_create(
    codename='view_visit',
    name='Can view visit',
    content_type=visit_content_type,)

#Изменение

change_doctor_permission = Permission.objects.get_or_create(
    codename='change_doctor',
    name='Can change doctor',
    content_type=doctor_content_type,)
change_patient_permission = Permission.objects.get_or_create(
    codename='change_patient',
    name='Can change patient',
    content_type=patient_content_type,)
change_ticket_permission = Permission.objects.get_or_create(
    codename='change_ticket',
    name='Can change tickets',
    content_type=ticket_content_type,)
change_diagnosis_permission = Permission.objects.get_or_create(
    codename='change_diagnosis',
    name='Can change diagnosis',
    content_type=diagnosis_content_type,)
change_neighborhood_permission = Permission.objects.get_or_create(
    codename='change_neighborhood',
    name='Can change neighborhood',
    content_type=neighborhood_content_type,)
change_visit_permission = Permission.objects.get_or_create(
    codename='change_visit',
    name='Can change visit',
    content_type=visit_content_type,)
change_diagnosis_in_ticket_permission = Permission.objects.get_or_create(
    codename='change_diagnosis_in_ticket',
    name='Can change diagnosis in ticket',
    content_type=ticket_content_type,
)

#Удаление

delete_doctor_permission = Permission.objects.get_or_create(
    codename='delete_doctor',
    name='Can delete doctor',
    content_type=doctor_content_type,)
delete_patient_permission = Permission.objects.get_or_create(
    codename='delete_patient',
    name='Can delete patient',
    content_type=patient_content_type,)
delete_ticket_permission = Permission.objects.get_or_create(
    codename='delete_ticket',
    name='Can delete tickets',
    content_type=ticket_content_type,)
delete_diagnosis_permission = Permission.objects.get_or_create(
    codename='delete_diagnosis',
    name='Can delete diagnosis',
    content_type=diagnosis_content_type,)
delete_neighborhood_permission = Permission.objects.get_or_create(
    codename='delete_neighborhood',
    name='Can delete neighborhood',
    content_type=neighborhood_content_type,)
delete_visit_permission = Permission.objects.get_or_create(
    codename='delete_visit',
    name='Can delete visit',
    content_type=visit_content_type,)

#Добавление

add_doctor_permission = Permission.objects.get_or_create(
    codename='add_doctor',
    name='Can add doctor',
    content_type=doctor_content_type,)
add_patient_permission = Permission.objects.get_or_create(
    codename='add_patient',
    name='Can add patient',
    content_type=patient_content_type,)
add_ticket_permission = Permission.objects.get_or_create(
    codename='add_ticket',
    name='Can add tickets',
    content_type=ticket_content_type,)
add_diagnosis_permission = Permission.objects.get_or_create(
    codename='add_diagnosis',
    name='Can add diagnosis',
    content_type=diagnosis_content_type,)
add_neighborhood_permission = Permission.objects.get_or_create(
    codename='add_neighborhood',
    name='Can add neighborhood',
    content_type=neighborhood_content_type,)
add_visit_permission = Permission.objects.get_or_create(
    codename='add_visit',
    name='Can add visit',
    content_type=visit_content_type,)

admin_permission = Permission.objects.filter(codename__in=['view_doctor', 'view_neighborhood','view_patient','view_ticket','view_diagnosis','view_visit',
                                                           'add_doctor','add_patient','add_ticket','add_diagnosis','add_neighborhood','add_visit',
                                                           'delete_doctor','delete_patient','delete_ticket','delete_diagnosis','delete_neighborhood','delete_visit',
                                                           'change_doctor','change_patient','change_ticket','change_diagnosis','change_neighborhood','change_visit'])
doctor_permission = Permission.objects.filter(codename__in=['view_doctor', 'view_patient','view_ticket','view_diagnosis','change_ticket','change_diagnosis_in_ticket'])
patient_permission = Permission.objects.filter(codename__in=['view_doctor', 'view_neighborhood'])
reception_permission = Permission.objects.filter(codename__in=['view_patient', 'view_neighborhood','add_neighborhood','delete_neighborhood','change_neighborhood','view_ticket','add_ticket','delete_ticket','change_ticket'])


DoctorGroup.permissions.set(doctor_permission)
PatientGroup.permissions.set(patient_permission)
AdminGroup.permissions.set(admin_permission)
ReceptionGroup.permissions.set(reception_permission)
'''
first = User.objects.filter(username='doctor_A')[0]
first.groups.add(DoctorGroup)

user_pat = User.objects.create_user(username='patient_A', password='mypassword')
user_pat.groups.add(PatientGroup)

user_rec = User.objects.create_user(username='recept_A', password='mypassword')
user_rec.groups.add(ReceptionGroup)

user_adm = User.objects.create_user(username='admin_A', password='mypassword')
user_adm.groups.add(AdminGroup)
'''