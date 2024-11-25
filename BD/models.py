from django.db import models

class Patient(models.Model):
    class Sex(models.TextChoices):
        Man = "Мужчина"
        Woman = "Женщина"
    id = models.IntegerField(primary_key=True)
    med_card = models.BigIntegerField()
    med_polys = models.BigIntegerField()
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    third_name = models.CharField(max_length=30,blank=True)
    sex = models.CharField(max_length=10,choices=Sex,default=Sex.Man)
    date_of_birth = models.DateField()
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=10)
    class Meta:
        managed = False
        db_table = 'Patient'
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

class Neighborhood(models.Model):
    id = models.IntegerField(primary_key=True)
    neighborhood_street = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'Neighborhood'
        verbose_name = "Район"
        verbose_name_plural = "Районы"

class Diagnosis(models.Model):
    id = models.IntegerField(primary_key=True)
    diagnosis = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'Diagnosis'
        verbose_name = "Диагноз"
        verbose_name_plural = "Диагнозы"

class Visit(models.Model):
    id = models.IntegerField(primary_key=True)
    visit = models.CharField(max_length=50)
    class Meta:
        managed = False
        db_table = 'Visit'
        verbose_name = "Цель визита"
        verbose_name_plural = "Цели визита"

class Doctor(models.Model):
    class Category(models.TextChoices):
        First = "Первая"
        Second = "Вторая"
        High = "Высшая"
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    third_name = models.CharField(max_length=30,blank=True)
    speciality = models.CharField(max_length=50)
    category = models.CharField(max_length=10,choices=Category,blank=True)
    salary = models.DecimalField(max_digits=8,decimal_places=2)
    neighborhood = models.ForeignKey(Neighborhood,models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'Doctor'
        verbose_name = "Доктор"
        verbose_name_plural = "Доктора"

class Ticket(models.Model):
    class Status(models.TextChoices):
        Primary = "Первичный"
        Secondary = "Вторичный"
    id = models.IntegerField(primary_key=True)
    date_n_time = models.DateTimeField()
    doctor = models.ForeignKey(Doctor,models.DO_NOTHING)
    patient = models.ForeignKey(Patient,models.DO_NOTHING)
    visit = models.ForeignKey(Visit,models.DO_NOTHING)
    diagnosis = models.ForeignKey(Diagnosis,models.DO_NOTHING,blank=True)
    status = models.CharField(max_length=10,choices=Status)
    class Meta:
        managed = False
        db_table = 'Ticket'
        verbose_name = "Талон"
        verbose_name_plural = "Талоны"
        unique_together = [['id', 'date_n_time']]