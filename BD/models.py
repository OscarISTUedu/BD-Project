from django.contrib.auth.views import UserModel
from django.db import models

class Patient(models.Model):
    class Sex(models.TextChoices):
        Man = "Мужчина"
        Woman = "Женщина"
    id = models.IntegerField(primary_key=True,verbose_name="Номер")
    med_card = models.BigIntegerField(verbose_name="Номер мед.карты")
    med_polys = models.BigIntegerField(verbose_name="Номер мед.полиса")
    name = models.CharField(max_length=20,verbose_name="Имя")
    surname = models.CharField(max_length=30,verbose_name="Фамилия")
    third_name = models.CharField(max_length=30,null=True,blank=True,verbose_name="Отчество")
    sex = models.CharField(max_length=10,choices=Sex,default=Sex.Man,verbose_name="Пол")
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    street = models.CharField(max_length=100,verbose_name="Улица")
    house = models.CharField(max_length=10,verbose_name="Дом")
    class Meta:
        managed = False
        db_table = 'Patient'
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

class Neighborhood(models.Model):
    id = models.IntegerField(primary_key=True,verbose_name="Номер")
    neighborhood_street = models.CharField(max_length=100,verbose_name="Улица")
    class Meta:
        managed = False
        db_table = 'Neighborhood'
        verbose_name = "Участок"
        verbose_name_plural = "Участки"

class Diagnosis(models.Model):
    id = models.IntegerField(primary_key=True,verbose_name="Номер")
    diagnosis = models.CharField(max_length=100,verbose_name="Диагноз")
    class Meta:
        managed = False
        db_table = 'Diagnosis'
        verbose_name = "Диагноз"
        verbose_name_plural = "Диагнозы"

class Visit(models.Model):
    id = models.IntegerField(primary_key=True,verbose_name="Номер")
    visit = models.CharField(max_length=50,verbose_name="Цель визита")
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
    id = models.IntegerField(primary_key=True,verbose_name="Номер")
    name = models.CharField(max_length=20,verbose_name="Имя")
    surname = models.CharField(max_length=30,verbose_name="Фамилия")
    third_name = models.CharField(max_length=30,blank=True,null=True,verbose_name="Отчество")
    speciality = models.CharField(max_length=50,verbose_name="Специальность")
    category = models.CharField(max_length=10,choices=Category,blank=True,verbose_name="Категория")
    salary = models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Зарплата")
    neighborhood = models.ForeignKey(Neighborhood,models.DO_NOTHING,verbose_name="Номер района")
    class Meta:
        managed = False
        db_table = 'Doctor'
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

class Ticket(models.Model):
    class Status(models.TextChoices):
        Primary = "Первичный"
        Secondary = "Вторичный"
    id = models.IntegerField(primary_key=True,verbose_name="Номер")
    date_n_time = models.DateTimeField(verbose_name="Дата и время приёма")
    doctor = models.ForeignKey(Doctor,models.DO_NOTHING,verbose_name="Номер доктора")
    patient = models.ForeignKey(Patient,models.DO_NOTHING,verbose_name="Номер пациента")
    visit = models.ForeignKey(Visit,models.DO_NOTHING,verbose_name="Номер цели посещения")
    diagnosis = models.ForeignKey(Diagnosis,models.DO_NOTHING,null=True,blank=True,verbose_name="Номер диагноза")
    status = models.CharField(max_length=10,choices=Status,verbose_name="Статус")
    class Meta:
        managed = False
        db_table = 'Ticket'
        verbose_name = "Талон"
        verbose_name_plural = "Талоны"
        #unique_together = [['id', 'date_n_time']]