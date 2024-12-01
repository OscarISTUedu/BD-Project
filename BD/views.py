import json

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from django.apps import apps
from .models import Patient, Doctor, Neighborhood, Diagnosis, Visit, Ticket

@permission_required('BD.view_patient')
def patient_list(request):
    patients = Patient.objects.all().order_by('id').values()
    fields = Patient._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': patients,'h1':Patient._meta.verbose_name_plural,'fields':fields})

@permission_required('BD.view_doctor')
def doctor_list(request):
    doctors = Doctor.objects.all().order_by('id').values()
    fields = Doctor._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': doctors, 'h1': Doctor._meta.verbose_name_plural, 'fields': fields})

@permission_required('BD.view_neighborhood')
def neighborhood_list(request):
    neighborhoods = Neighborhood.objects.all().order_by('id').values()
    fields = Neighborhood._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': neighborhoods, 'h1': Neighborhood._meta.verbose_name_plural, 'fields': fields})

@permission_required('BD.view_diagnosis')
def diagnoses_list(request):
    diagnoses = Diagnosis.objects.all().order_by('id').values()
    fields = Diagnosis._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': diagnoses, 'h1': Diagnosis._meta.verbose_name_plural, 'fields': fields})

@permission_required('BD.view_visit')
def visit_list(request):
    visits = Visit.objects.all().order_by('id').values()
    fields = Visit._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': visits, 'h1': Visit._meta.verbose_name_plural, 'fields': fields})

@permission_required('BD.view_ticket')
def ticket_list(request):
    tickets = Ticket.objects.all().order_by('id').values()
    fields = Ticket._meta.get_fields()
    return render(request, 'model_list.html',
                  {'models': tickets, 'h1': Ticket._meta.verbose_name_plural, 'fields': fields})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def main_view(request):
    return render(request, 'main.html')

@login_required
def change_view(request):
    data = json.loads(request.body)
    new_data = data.pop('new_data')
    last_data = data.pop('last_data')
    if new_data==last_data:
        return HttpResponse(status=304)
    verbose_name_plural = data.pop('table_verbose_name_plural')
    verbose_name_field = data.pop('field_name')
    row_id = data.pop('id')
    for model in apps.get_models():
        if model._meta.verbose_name_plural == verbose_name_plural:
            cur_model = model
            break
    fields = cur_model._meta.get_fields()
    for field in fields:
        if field.get_internal_type()!="ForeignKey":
            if field.verbose_name == verbose_name_field:
                cur_field = field.name
                break
    cur_obj = cur_model.objects.filter(id=row_id).first()
    if cur_obj:
        setattr(cur_obj, cur_field, new_data)
        try:
            cur_obj.full_clean()
            cur_obj.save()
        except ValidationError as e:
            return JsonResponse({"response":e.messages[0]},status=500)
    else:
        return JsonResponse({'error_message': cur_model+" с id="+row_id+" не существует"},status=500)
    return HttpResponse(status=200)

def patient_for_doctor(patient_street,doctor_neighbourhood_id):
    '''
    patient_street - улица пациента
    doctor_neighbourhood_id - участок врача
    Проверка совпадает ли улица в участке врача с улицой пациента
    '''
    cur_pat = Patient.object.filter(street=patient_street).first()
    if not cur_pat:
        return False
    cur_nei_doctor = Neighborhood.object.filter(id=doctor_neighbourhood_id).first()
    if not cur_nei_doctor:
        return False
    cur_street_doctor = cur_nei_doctor.street
    if (patient_street==cur_street_doctor):
        return True
    return False