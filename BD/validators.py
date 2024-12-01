import re
from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
    print(value_str)
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
    pattern = r'^\d{2}-\d{2}-\d{4}$'  # Формат "дд-мм-гггг"
    if not (re.fullmatch(pattern, value)):
        raise ValidationError("Не верный формат")
