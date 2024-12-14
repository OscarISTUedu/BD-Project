from django.core.validators import DecimalValidator
from django.db import models

from BD.validators import validate_house, validate_street, validate_birth, validate_third_name, validate_surname, \
    validate_name, validate_speciality, validate_street_neighborhood, validate_diagnosis, validate_visit


class Patient(models.Model):
    class Sex(models.TextChoices):
        Man = "Мужчина"
        Woman = "Женщина"
    id = models.IntegerField(primary_key=True,verbose_name="Номер")
    med_card = models.BigIntegerField(verbose_name="Номер мед.карты")
    med_polys = models.BigIntegerField(verbose_name="Номер мед.полиса")
    name = models.CharField(max_length=20,verbose_name="Имя",validators=[validate_name])
    surname = models.CharField(max_length=30,verbose_name="Фамилия",validators=[validate_surname])
    third_name = models.CharField(max_length=30,null=True,blank=True,verbose_name="Отчество",validators=[validate_third_name])
    sex = models.CharField(max_length=10,choices=Sex,verbose_name="Пол")
    date_of_birth = models.DateField(verbose_name="Дата рождения",validators=[validate_birth])
    street = models.CharField(max_length=100,verbose_name="Улица",validators=[validate_street])
    house = models.CharField(max_length=10,verbose_name="Дом",validators=[validate_house])
    class Meta:
        managed = False
        db_table = 'Patient'
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

class Neighborhood(models.Model):
    id = models.IntegerField(primary_key=True,verbose_name="Номер")
    neighborhood_street = models.CharField(max_length=100,verbose_name="Улица",unique=True,validators=[validate_street_neighborhood])
    class Meta:
        managed = False
        db_table = 'Neighborhood'
        verbose_name = "Участок"
        verbose_name_plural = "Участки"

class Diagnosis(models.Model):
    id = models.IntegerField(primary_key=True,verbose_name="Номер")
    diagnosis = models.CharField(max_length=100,verbose_name="Диагноз",unique=True,validators=[validate_diagnosis])
    class Meta:
        managed = False
        db_table = 'Diagnosis'
        verbose_name = "Диагноз"
        verbose_name_plural = "Диагнозы"

class Visit(models.Model):
    id = models.IntegerField(primary_key=True,verbose_name="Номер")
    visit = models.CharField(max_length=50,verbose_name="Цель визита",unique=True,validators=[validate_visit])
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
    name = models.CharField(max_length=20,verbose_name="Имя",validators=[validate_name])
    surname = models.CharField(max_length=30,verbose_name="Фамилия",validators=[validate_surname])
    third_name = models.CharField(max_length=30,blank=True,null=True,verbose_name="Отчество",validators=[validate_third_name])
    speciality = models.CharField(max_length=50,verbose_name="Специальность",validators=[validate_speciality])
    category = models.CharField(max_length=10,choices=Category,blank=True,null=True,verbose_name="Категория")
    salary = models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Зарплата",validators=[DecimalValidator(max_digits=8,decimal_places=2)])
    neighborhood = models.ForeignKey(Neighborhood,on_delete=models.PROTECT,verbose_name="Номер района",related_name='doctor')
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
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,verbose_name="Врач,номер")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,verbose_name="Пациент,номер")
    visit = models.ForeignKey(Visit,on_delete=models.CASCADE,verbose_name="Цель посещения",related_name="visit_id")
    diagnosis = models.ForeignKey(Diagnosis,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Диагноз")
    status = models.CharField(max_length=10,choices=Status,verbose_name="Статус")
    class Meta:
        managed = False
        db_table = 'Ticket'
        verbose_name = "Талон"
        verbose_name_plural = "Талоны"
        unique_together = [['id', 'date_n_time']]