from django.shortcuts import render
from .models import Patient

def patient_list(request):
    # Получаем все записи пациентов
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})