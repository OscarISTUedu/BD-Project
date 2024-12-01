import re
from datetime import datetime

from django.core.exceptions import ValidationError

#Валидация Пациента
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