from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
DoctorGroup = Group.objects.create(name='DoctorGroup')
PatientGroup = Group.objects.create(name='PatientGroup')
AdminGroup = Group.objects.create(name='AdminGroup')
ReceptionGroup = Group.objects.create(name='ReceptionGroup')

DoctorReadPermission = Permission.objects.create()

user = User.objects.create_user('doctor', 'myemail@crazymail.com', 'mypassword')
user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

# Обновите поля и сохраните их снова
user.first_name = 'John'
user.last_name = 'Citizen'
user.save()