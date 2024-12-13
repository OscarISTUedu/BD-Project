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

def validate_status(field_name,cur_obj,new_data,new_row):
    from BD.models import Ticket
    from django.http import JsonResponse
    if field_name == "status":
        if cur_obj is not None:
            cur_pat = cur_obj.patient
            cur_doc = cur_obj.doctor
            tickets_for_cur_pat = Ticket.objects.filter(patient=cur_pat,doctor=cur_doc)  # другие записи у данного пациента к данному врачу
            tickets_for_cur_pat = tickets_for_cur_pat.filter(date_n_time__gt=cur_obj.date_n_time) #записи которые были ранее
            tickets_for_cur_pat = tickets_for_cur_pat.filter(diagnosis__isnull=False) #записи в которых есть диагноз (значит был прошлый приём)
            if tickets_for_cur_pat.exists() and new_data == "Первичный":  # если предыдущие записи не найдены, значит данный приём первичный
                return JsonResponse({"response": "Статус не может быть первичным,данный пациент уже посещал этого врача"}, status=500)
            if not tickets_for_cur_pat.exists() and new_data == "Вторичный":
                return JsonResponse({"response": "Статус не может быть вторичный,данный пациент ещё не посещал этого врача"},status=500)
        else:
            diagnosis_id = new_row.get('diagnosis_id')
            patient_id = new_row.get('patient_id')
            doctor_id = new_row.get('doctor_id')
            date_n_time = new_row.get('date_n_time')
            if all([diagnosis_id,patient_id,doctor_id,date_n_time]):
                tickets_for_cur_pat = Ticket.objects.filter(patient=patient_id,doctor=doctor_id)  # другие записи у данного пациента к данному врачу
                tickets_for_cur_pat = tickets_for_cur_pat.filter(date_n_time__gt=date_n_time)  # записи которые были ранее
                tickets_for_cur_pat = tickets_for_cur_pat.filter(diagnosis__isnull=False)  # записи в которых есть диагноз (значит был прошлый приём)
                if tickets_for_cur_pat.exists() and new_data == "Первичный":  # если предыдущие записи не найдены, значит данный приём первичный
                    print(tickets_for_cur_pat)
                    return JsonResponse({"response": "Статус не может быть первичным,данный пациент уже посещал этого врача"}, status=500)
                if not tickets_for_cur_pat.exists() and new_data == "Вторичный":
                    return JsonResponse({"response": "Статус не может быть вторичный,данный пациент ещё не посещал этого врача"},status=500)
    else:
        return None

def validate_patient_id(field_name,childModels,field_id,cur_obj,new_row):
    from django.http import JsonResponse
    from BD.models import Doctor, Neighborhood
    if field_name == "patient_id":
        if cur_obj is not None:#если это есть в бд, то берём инфу оттуда
            # меняем пациента у текущего доктора, берём улицу нового пациента, берём район текущего доктора, из этого района берём улицу сравниваем эту улицу и улицу у текущего пациента
            pat_street = childModels.objects.filter(id=field_id).first().street
            doc_surname = Doctor.objects.filter(id=cur_obj.doctor.id).first().surname
            doc_street = Neighborhood.objects.filter(id=cur_obj.doctor.neighborhood.id).first().neighborhood_street
            if not pat_street == doc_street:  # childModels - Пациент
                print(pat_street,doc_street)
                return JsonResponse({"response": f"Данный пациент не сможет ходить на приём к доктору {doc_surname} т.к он не принимает этот район"}, status=500)
        else:
            doctor_id = new_row.get('doctor_id')
            if doctor_id is not None:#Если доктор задан, то проверяем пациента
                neighborhood_id = Doctor.objects.filter(id = int(doctor_id)).first().neighborhood.id
                doc_surname = Doctor.objects.filter(id=doctor_id).first().surname
                pat_street = childModels.objects.filter(id=field_id).first().street
                doc_street = Neighborhood.objects.filter(id=neighborhood_id).first().neighborhood_street
                if not pat_street == doc_street:
                    print(pat_street,doc_street)
                    return JsonResponse({"response": f"Данный пациент не сможет ходить на приём к доктору {doc_surname} т.к он не принимает этот район"},status=500)
    else:
        return None

def validate_doctor_id(field_name,childModels,field_id,cur_obj,new_row):
    from django.http import JsonResponse
    from BD.models import Patient
    if field_name == "doctor_id":
        if cur_obj is not None:  # если это есть в бд, то берём инфу оттуда
            # меняем доктора у текущего пациента, берём район нового доктора из этого района берём улицу, сравниваем эту улицу и улицу у текущего пациента
            pat_street = Patient.objects.filter(id=cur_obj.patient.id).first().street
            pat_surname = Patient.objects.filter(id=cur_obj.patient.id).first().surname
            doc_street = childModels.objects.filter(id=field_id).first().neighborhood.neighborhood_street
            if not pat_street == doc_street:  # childModels - Доктор
                return JsonResponse({"response": f"Данный доктор не сможет обслужить пациента {pat_surname} т.к он живёт в другом районе"},status=500)
        else:
            patient_id = new_row.get('patient_id')
            if patient_id is not None:  # Если доктор задан, то проверяем пациента
                patient_id = int(patient_id)
                pat_street = Patient.objects.filter(id=patient_id).first().street
                pat_surname = Patient.objects.filter(id=patient_id).first().surname
                doc_street = childModels.objects.filter(id=field_id).first().neighborhood.neighborhood_street
                if not pat_street == doc_street:
                    return JsonResponse({"response": f"Данный доктор не сможет обслужить пациента {pat_surname} т.к он живёт в другом районе"},status=500)
    else:
        return None

def validate_empty(data,cur_model,new_row):#проверка поля, его нет в бд
    from django.http import JsonResponse
    from types import NoneType
    new_data = data.get('new_data')
    #last_data = data.get('last_data')
    #model_name = data.get('model_name')
    field_name = data.get('field_name')
    type = data.get('type')
    new_row = data.get('new_row')
    #row_id = data.get('id')
    field = cur_model._meta.get_field(field_name)
    if type == "text&id":
        field_id = data.get('field_id')#id в родительской таблице
        field_id = None if new_data=="-" else field_id
        relatedModel = cur_model._meta.get_field(field_name).related_model
        validated_patient_id = validate_patient_id(field_name,relatedModel,field_id,None,new_row)
        if not isinstance(validated_patient_id,NoneType):
            return validated_patient_id
        validated_doctor_id = validate_doctor_id(field_name,relatedModel,field_id,None,new_row)
        if not isinstance(validated_doctor_id,NoneType):
            return validated_doctor_id
        try:
            field.clean(field_id,None)
        except Exception as e:
            return JsonResponse({"response": f"Значение {field_id} не найдено в родительской таблице,возможно проблема в некоректной форме"},status=500)
    else:
        new_data = None if new_data == "-" else new_data

        validated_status = validate_status(field_name,None,new_data,new_row)
        if not isinstance(validated_status,NoneType):
            return validated_status
        try:
            field.clean(new_data, None)
        except Exception as e:
            return JsonResponse({"response": f"Значение {new_data} не найдено в родительской таблице,возможно проблема в некоректной форме"},status=500)
    return JsonResponse({"key":field_name,"value":field_id},status=200) if type == "text&id" else JsonResponse({"key":field_name,"value":new_data},status=200)



