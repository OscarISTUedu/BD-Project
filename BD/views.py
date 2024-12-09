import datetime
import json
from idlelib.config_key import translate_key

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import ManyToOneRel, ForeignKey
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
    Patient.objects.filter()
    fields = Ticket._meta.get_fields()
    for ticket in tickets:
        if ticket.get('diagnosis_id'):
            diagnosis = Diagnosis.objects.filter(id=ticket.get('diagnosis_id')).first().diagnosis
        else:
            diagnosis = None
        visit = Visit.objects.filter(id=ticket.get('visit_id')).first().visit
        patient = Patient.objects.filter(id=ticket.get('patient_id')).first().surname
        doctor = Doctor.objects.filter(id=ticket.get('doctor_id')).first().surname
        ticket['diagnosis_id'] = diagnosis
        ticket['visit_id'] =  visit
        ticket['patient_id'] = patient +","+"№"+str(ticket['patient_id'])
        ticket['doctor_id'] = doctor +","+ "№"+str(ticket['doctor_id'])
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
    data_all = data.copy()
    request_type = data.pop('field')
    new_data = data.pop('new_data')
    if request_type == "text":
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
    is_foreign_key = False
    fields = cur_model._meta.get_fields()
    for field in fields:
        if not isinstance(field, ManyToOneRel):
            if field.verbose_name == verbose_name_field:
                if isinstance(field, ForeignKey):
                    is_foreign_key = True
                cur_field_name = field.name
                cur_field = field
                break
    cur_obj = cur_model.objects.filter(id=row_id).first()
    if cur_obj:#если сущ-ет то меняем, если нет то добавляем
        if  is_foreign_key:
            childModel_name_plural = getattr(cur_obj, cur_field_name)._meta.verbose_name_plural
            for model in apps.get_models():
                if model._meta.verbose_name_plural == childModel_name_plural:
                    childModels = model
                    break
            try:
                can_update = childModels.objects.filter(id=new_data).exists()
            except ValueError as e:
                return JsonResponse({"response": "Не верный формат данных"}, status=500)
            if not can_update:
                return JsonResponse({"response": "Данной записи в дочерней таблице не существует"}, status=500)
            if cur_field_name == "doctor":
                #меняем доктора у текущего пациента, берём район нового доктора из этого района берём улицу, сравниваем эту улицу и улицу у текущего пациента
                pat_street = Patient.objects.filter(id=cur_obj.patient.id).first().street
                pat_surname = Patient.objects.filter(id=cur_obj.patient.id).first().surname
                doc_street = childModels.objects.filter(id=new_data).first().neighborhood.neighborhood_street
                if not pat_street==doc_street:#childModels - Доктор
                    return JsonResponse({"response": f"Данный доктор не сможет обслужить пациента {pat_surname} т.к пациент живёт в другом районе"}, status=500)

            if cur_field_name == "patient":
                #меняем пациента у текущего доктора, берём улицу нового пациента,берём район текущего доктора, из этго района берём улицу сравниваем эту улицу и улицу у текущего пациента
                pat_street = childModels.objects.filter(id=new_data).first().street
                doc_surname = Doctor.objects.filter(id=cur_obj.doctor.id).first().surname
                doc_street = Neighborhood.objects.filter(id=cur_obj.doctor.id).first().neighborhood_street
                if not pat_street==doc_street:#childModels - Пациент
                    return JsonResponse({"response": f"Данный пациент не сможет ходить на приём к доктору {doc_surname} т.к доктор не принимает этот район"}, status=500)

            if cur_field_name == "neighborhood":#Изменение района для доктора, означает что все его записи для людей старого района удаляются
                Ticket.objects.filter(doctor = cur_obj.id).delete()
            child_instance = childModels.objects.filter(id=new_data).first()
            try:
                setattr(cur_obj, cur_field_name, child_instance)
            except Exception as e:
                return JsonResponse({"response": f"Значение {new_data} не найдено в дочерней таблице,возмонжо проблема в некоректной форме"},status=500)
            try:
                cur_obj.full_clean()
                cur_obj.save()
            except ValidationError as e:
                return JsonResponse({"response": e.messages[0]}, status=500)
            return HttpResponse(status=200)
        if cur_field=="status":
            cur_pat = cur_obj.patient
            cur_doc = cur_obj.doctor
            tickets_for_cur_pat = Ticket.objects.filter(patient=cur_pat,doctor = cur_doc)
            if tickets_for_cur_pat.exists() and new_data=="Первичный":#если предыдущие записи не найдены, значит данный приём первичный
                return JsonResponse({"response": "Статус не может быть вторичный,данный пациент не посещял этого врача"}, status=500)
            for ticket in tickets_for_cur_pat:#если найдены предыдущие записи у того же врача,у них есть диагноз значит данный приём вторичный
                if not (ticket.diagnosis and new_data== "Вторичный"):
                    return JsonResponse({"response": "Статус не может быть первичным,данный пациент уже посещял этого врача"}, status=500)
        try:
            setattr(cur_obj, cur_field_name, new_data)
        except Exception as e:
            print(str(e))
            return JsonResponse({"response": f"Значение {new_data} не найдено в дочерней таблице,возмонжо проблема в некоректной форме"}, status=500)
        try:
            cur_obj.full_clean()
            cur_obj.save()
        except ValidationError as e:
            return JsonResponse({"response":e.messages[0]},status=500)
    else:
        return JsonResponse({'error_message': str(cur_model) + " с id="+row_id+" не существует"},status=500)
    return HttpResponse(status=200)

def add_empty_row(request):
    data = json.loads(request.body)
    verbose_name_plural = data.pop('table_verbose_name_plural')
    for model in apps.get_models():
        if model._meta.verbose_name_plural == verbose_name_plural:
            cur_model = model
            break
    last_obj = cur_model.objects.last().id
    return JsonResponse({"id":last_obj+1},status=200)

def validate_field (request):
    data = json.loads(request.body)
    verbose_name_plural = data.pop('table_verbose_name_plural')
    verbose_name_field = data.pop('field_name')
    new_data = data.pop('new_data')
    for model in apps.get_models():
        if model._meta.verbose_name_plural == verbose_name_plural:
            cur_model = model
            break
    fields = cur_model._meta.get_fields()
    for field in fields:
        if not isinstance(field, ManyToOneRel):
            if field.verbose_name == verbose_name_field:
                if isinstance(field, ForeignKey):
                    is_foreign_key = True
                cur_field_name = field.name
                cur_field = field
                break
    cur_obj = cur_model.create()
    try:
        setattr(cur_obj, cur_field_name, new_data)
    except Exception as e:
        print(str(e))
        cur_obj.delete()
        return JsonResponse(
            {"response": f"Значение {new_data} не найдено в дочерней таблице,возмонжо проблема в некоректной форме"},
            status=500)
    cur_obj.delete()
    return JsonResponse ({cur_field_name:new_data},status=200)

def get_fields_by_name(request):
    data = json.loads(request.body)
    field_name = data.pop('field_name')
    model_name = data.pop('model_name')
    for model in apps.get_models():
        if model._meta.verbose_name_plural == model_name:
            cur_model = model
            break
    values = cur_model.objects.values_list(field_name,flat=True).distinct()
    values = [val for val in values]
    return JsonResponse({"values": values}, status=200)
