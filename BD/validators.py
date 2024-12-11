import re
from datetime import datetime

from django.core.exceptions import ValidationError

#Валидация адреса пациента
def validate_house(value):
    pattern = r'^[0-9]+[А-Яа-яЁё]*$'
    if not(re.match(pattern, value)):
        raise ValidationError("Не верный номер дома")

def validate_street(value):
    pattern = r'^[А-Яа-яЁёA-Za-z\s]+(,\s*\d+)?$'
    if not(re.match(pattern, value)):
        raise ValidationError("Не верный формат")
    from BD.models import Neighborhood
    if not(Neighborhood.objects.filter(neighborhood_street=value).first()):
        raise ValidationError("Нет такой улицы")

#Валидация адреса участка
def validate_street_neighborhood(value):
    pattern = r'^[А-Яа-яЁёA-Za-z\s]+(,\s*\d+)?$'
    if not(re.match(pattern, value)):
        raise ValidationError("Не верный формат")

#Валидация даты
def validate_birth(value):
    value_str = str(value)
    pattern = r'^\d{4}-\d{2}-\d{2}$'  # Формат "дд-мм-гггг"
    if not (re.fullmatch(pattern, value_str)):
        raise ValidationError("Не верный формат")
    year, month, day = value_str.split('-')
    if year.isdigit() and month.isdigit() and day.isdigit():
        year = int(year)
        month = int(month)
        day = int(day)
        try:
            datetime.strptime(value_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Не верный формат")
        if not (1900 < year < datetime.now().year):
            raise ValidationError("Не верно указан год")
        if not(0 < month < 13):
            raise ValidationError("Не верно указан месяц")
        if not(0 < day < 32):
            raise ValidationError("Не верно указан месяц")
    else:
        raise ValidationError("Не верный формат")

#Валидация ФИО
def validate_third_name(value):
    pattern = r'^[А-ЯЁ][а-яё]+(вич|вна|ич|ична|ович|овна)$'
    if not (re.fullmatch(pattern, value)):
        raise ValidationError("Не верный формат")

def validate_surname(value):
    pattern = r'^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$'  # Поддержка двойных фамилий через дефис
    if not (re.fullmatch(pattern, value)):
        raise ValidationError("Не верный формат")

def validate_name(value):
    pattern = r'^[А-ЯЁ][а-яё]+$'
    if not (re.fullmatch(pattern, value)):
        raise ValidationError("Не верный формат")

#Валидация Врача
def validate_speciality(value):
    pattern = r'^[А-ЯЁа-яё]+(\s?\([А-ЯЁа-яё\s-]+\))?$'
    if not (re.fullmatch(pattern, value)):
        raise ValidationError("Не верный формат")

#Валидация Диагноза
def validate_diagnosis(value):
    pattern = r'.*(\b[А-Яа-яЁёA-Za-z0-9\s\-\,\.]+\b).*'
    if not (re.fullmatch(pattern, value)):
        raise ValidationError("Не верный формат")

def validate_visit(value):
    pattern = r'^[А-Яа-яЁё]+( [А-Яа-яЁё]+)*$'
    if not (re.fullmatch(pattern, value)):
        raise ValidationError("Не верный формат")

def validate_status(field_name,cur_obj,new_data):
    from BD.models import Ticket
    from django.http import JsonResponse
    if field_name == "status":
        cur_pat = cur_obj.patient
        cur_doc = cur_obj.doctor
        tickets_for_cur_pat = Ticket.objects.filter(patient=cur_pat,doctor=cur_doc)  # другие записи у данного пациента к данному врачу
        if tickets_for_cur_pat.exists() and new_data == "Первичный":  # если предыдущие записи не найдены, значит данный приём первичный
            return JsonResponse({"response": "Статус не может быть первичным,данный пациент уже посещал этого врача"}, status=500)
        if new_data == "Вторичный":
            for ticket in tickets_for_cur_pat:  # если найдены предыдущие записи у того же врача, у них есть диагноз значит данный приём вторичный
                if not ticket.diagnosis:
                    return JsonResponse({"response": "Статус не может быть вторичный,данный пациент ещё не посещал этого врача"},status=500)
    else:
        return None

def validate_patient_id(field_name,childModels,field_id,cur_obj):
    from django.http import JsonResponse
    from BD.models import Doctor, Neighborhood
    if field_name == "patient_id":
        # меняем пациента у текущего доктора, берём улицу нового пациента, берём район текущего доктора, из этого района берём улицу сравниваем эту улицу и улицу у текущего пациента
        pat_street = childModels.objects.filter(id=field_id).first().street
        doc_surname = Doctor.objects.filter(id=cur_obj.doctor.id).first().surname
        doc_street = Neighborhood.objects.filter(id=cur_obj.doctor.id).first().neighborhood_street
        if not pat_street == doc_street:  # childModels - Пациент
            return JsonResponse({"response": f"Данный пациент не сможет ходить на приём к доктору {doc_surname} т.к он не принимает этот район"},status=500)
    else:
        return None

def validate_doctor_id(field_name,childModels,field_id,cur_obj):
    from django.http import JsonResponse
    from BD.models import Patient
    if field_name == "doctor_id":
        # меняем доктора у текущего пациента, берём район нового доктора из этого района берём улицу, сравниваем эту улицу и улицу у текущего пациента
        pat_street = Patient.objects.filter(id=cur_obj.patient.id).first().street
        pat_surname = Patient.objects.filter(id=cur_obj.patient.id).first().surname
        doc_street = childModels.objects.filter(id=field_id).first().neighborhood.neighborhood_street
        if not pat_street == doc_street:  # childModels - Доктор
            return JsonResponse({"response": f"Данный доктор не сможет обслужить пациента {pat_surname} т.к он живёт в другом районе"},status=500)
    else:
        return None


