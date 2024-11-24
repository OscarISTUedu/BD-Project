from django.db import models

class Patient(models.Model):
    class Sex(models.TextChoices):
        Man = "Мужчина"
        Woman = "Женщина"
    med_card = models.IntegerField()
    med_polys = models.IntegerField()
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    third_name = models.CharField(max_length=30,Null=True)
    sex = models.CharField(max_length=10,choices=Sex,default=Sex.Man)
    date_of_birth = models.DateField()
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=10)

class Doctor(models.Model):
    class Category(models.TextChoices):
        First = "Первая"
        Second = "Вторая"
        High = "Высшая"
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    third_name = models.CharField(max_length=30,Null=True)
    speciality = models.CharField(max_length=50)
    category = models.CharField(max_length=10,choices=Category,Null=True)
    salary = models.DecimalField(max_digits=8,decimal_places=2)
    neighborhood = models.ForeignKey()

class Neighborhood(models.Model):
    neighborhood_street = models.CharField(max_length=100)

class Diagnosis(models.Model):
    diagnosis = models.CharField(max_length=100)

class Visit(models.Model):
    visit = models.CharField(max_length=50)

class Ticket(models.Model):
    class Status(models.TextChoices):
        Primary = "Первичный"
        Secondary = "Вторичный"
    date_n_time = models.DateTimeField()
    doctor = models.ForeignKey(Doctor,models.DO_NOTHING)
    patient = models.ForeignKey(Patient,models.DO_NOTHING)
    visit = models.ForeignKey(Visit,models.DO_NOTHING)
    diagnosis = models.ForeignKey(Diagnosis,models.DO_NOTHING,null=True)
    status = models.CharField(choices=Status)