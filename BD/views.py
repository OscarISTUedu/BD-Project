import json
from dataclasses import field
from types import NoneType

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import ManyToOneRel
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from django.apps import apps

from .models import Patient, Doctor, Neighborhood, Diagnosis, Visit, Ticket
from .validators import validate_status, validate_patient_id, validate_doctor_id, validate_empty


@permission_required('BD.view_patient')
def patient_list(request):
    patients = Patient.objects.all().order_by('id').values()
    fields = Patient._meta.get_fields()
    fields = fields[1:]

    return render(request, 'model_list.html',
                  {'models': patients,'h1':Patient._meta.verbose_name_plural,'fields':fields,"fields_len":len(fields)})

@permission_required('BD.view_doctor')
def doctor_list(request):
    doctors = Doctor.objects.all().order_by('id').values()
    fields = Doctor._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': doctors, 'h1': Doctor._meta.verbose_name_plural, 'fields': fields,"fields_len":len(fields)})

@permission_required('BD.view_neighborhood')
def neighborhood_list(request):
    neighborhoods = Neighborhood.objects.all().order_by('id').values()
    fields = Neighborhood._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': neighborhoods, 'h1': Neighborhood._meta.verbose_name_plural, 'fields': fields,"fields_len":len(fields)})

@permission_required('BD.view_diagnosis')
def diagnoses_list(request):
    diagnoses = Diagnosis.objects.all().order_by('id').values()
    fields = Diagnosis._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': diagnoses, 'h1': Diagnosis._meta.verbose_name_plural, 'fields': fields,"fields_len":len(fields)})

@permission_required('BD.view_visit')
def visit_list(request):
    visits = Visit.objects.all().order_by('id').values()
    fields = Visit._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': visits, 'h1': Visit._meta.verbose_name_plural, 'fields': fields,"fields_len":len(fields)})

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
                  {'models': tickets, 'h1': Ticket._meta.verbose_name_plural, 'fields': fields,"fields_len":len(fields)})

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

@login_required #Изменение текстовых полей
def change_view(request):
    data = json.loads(request.body)
    new_data = data.get('new_data')
    last_data = data.get('last_data')
    if new_data==last_data:
        return HttpResponse(status=304)
    verbose_name_plural = data.get('table_verbose_name_plural')
    verbose_name_field = data.get('field_name')
    row_id = data.get('id')
    for model in apps.get_models():
        if model._meta.verbose_name_plural == verbose_name_plural:
            cur_model = model
            break
    fields = cur_model._meta.get_fields()
    for field in fields:
        if not isinstance(field, ManyToOneRel):
            if field.verbose_name == verbose_name_field:
                cur_field_name = field.name
                break
    cur_obj = cur_model.objects.filter(id=row_id).first()
    if cur_obj:#если сущ-ет, то меняем, если нет, то
        try:
            setattr(cur_obj, cur_field_name, new_data)
        except Exception as e:
            return JsonResponse({"response": f"Значение {new_data} не найдено в дочерней таблице,возмонжо проблема в некоректной форме"}, status=500)
        try:
            cur_obj.full_clean()
            cur_obj.save()
        except ValidationError as e:
            return JsonResponse({"response":e.messages[0]},status=500)
    else:
        field = cur_model._meta.get_field(cur_field_name)
        try:
            field.clean(new_data, None)
        except Exception as e:
            return JsonResponse({"response": "Не верный формат"},status=500)
    return JsonResponse({"key":cur_field_name,"value":new_data},status=200)

@login_required
def add_empty_row(request):
    data = json.loads(request.body)
    verbose_name_plural = data.pop('table_verbose_name_plural')
    for model in apps.get_models():
        if model._meta.verbose_name_plural == verbose_name_plural:
            cur_model = model
            break
    last_obj = cur_model.objects.last().id
    return JsonResponse({"id":last_obj+1},status=200)

@login_required
def validate_field (request):#валидация любого поля, данной записи нет в бд, но есть в new_row
    data = json.loads(request.body)
    new_data = data.get('new_data')
    last_data = data.get('last_data')
    type = data.get('type')
    if new_data == last_data and ((type == "text&id" and new_data != "-") or (type == "id" and new_data != "-")):
        return HttpResponse(status=304)
    model_name = data.get('model_name')
    new_row = data.get('new_row')
    for model in apps.get_models():
        if model._meta.verbose_name_plural == model_name:
            cur_model = model
            break
    return validate_empty(data, cur_model, new_row)

@login_required
def get_fields_by_name(request):#все значения для выпадающего списка
    data = json.loads(request.body)
    field_name = data.pop('field_name')
    model_name = data.pop('model_name')
    for model in apps.get_models():
        if model._meta.verbose_name_plural == model_name:
            cur_model = model
            break
    relatedModel = cur_model._meta.get_field(field_name).related_model
    field_cut = field_name.split('_')
    if field_name in ["visit_id","diagnosis_id"]:#выводятся - названия, значения - id
        values = list(relatedModel.objects.values_list(field_cut[1],field_cut[0]))
        values = [item for item in values if item[0] is not None]#убрали None
        values.append((-1,"-")) if cur_model._meta.get_field(field_name).null and cur_model._meta.get_field(field_name).blank else None
        values = sorted(values, key=lambda x: x[0])
        return JsonResponse({"values": values,"type":"text&id"}, status=200)
    elif field_name in ["neighborhood_id"]:
        field_cut[0]+="_street"
        values = list(relatedModel.objects.values_list(field_cut[1],flat=True))
        values.sort()
        return JsonResponse({"values": values,"type":"id"}, status=200)
    else:#статус, категория, улица(пациента)
        values = cur_model.objects.values_list(field_name,flat=True).distinct()
    if field_name in ["doctor_id","patient_id"]:
        values = relatedModel.objects.values_list("id","surname")
        values = [item for item in values if item[0] is not None]
        values = [(value1,value2+",№"+str(value1)) for value1,value2 in values]
        values = sorted(values, key=lambda x: x[0])
        return JsonResponse({"values": values, "type": "text&id"}, status=200)
    try:
        values = [int(val) for val in values]
    except Exception:
        values = [val for val in values]
    values.sort()
    return JsonResponse({"values": values,"type":"id"}, status=200)

@login_required
def change_by_list(request):#изменение (не)существующей записи в бд, её валидация
    data = json.loads(request.body)
    new_data = data.get('new_data')
    last_data = data.get('last_data')
    type = data.get('type')
    if new_data == last_data and ((type == "text&id" and new_data!="-") or (type == "id" and new_data!="-")):
        return HttpResponse(status=304)
    model_name = data.get('model_name')
    field_name = data.get('field_name')
    row_id = data.get('id')
    for model in apps.get_models():
        if model._meta.verbose_name_plural == model_name:
            cur_model = model
            break
    cur_obj = cur_model.objects.filter(id=row_id).first()
    if type == "text&id":
        field_id = data.get('field_id')#id в родительской таблице
        field_id = None if new_data=="-" else field_id
        relatedModel = cur_model._meta.get_field(field_name).related_model
        validated_patient_id = validate_patient_id(field_name,relatedModel,field_id,cur_obj,{})
        if not isinstance(validated_patient_id,NoneType):
            return validated_patient_id
        validated_doctor_id = validate_doctor_id(field_name,relatedModel,field_id,cur_obj,{})
        if not isinstance(validated_doctor_id,NoneType):
            return validated_doctor_id
        try:
            setattr(cur_obj, field_name, field_id)
        except Exception as e:
            return JsonResponse(
                {"response": f"Значение {field_id} не найдено в родительской таблице,возможно проблема в некоректной форме"},
                status=500)
    else:
        new_data = None if new_data == "-" else new_data
        validated_status = validate_status(field_name,cur_obj,new_data,{})#Проверка валидности поля status
        if not isinstance(validated_status,NoneType):
            return validated_status
        try:
            setattr(cur_obj, field_name, new_data)
        except Exception as e:
            return JsonResponse(
                {"response": f"Значение {new_data} не найдено в родительской таблице,возможно проблема в некоректной форме"},
                status=500)
    try:
        cur_obj.full_clean()
        cur_obj.save()
    except ValidationError as e:
        return JsonResponse({"response": e.messages[0]}, status=500)
    return JsonResponse({},status=200)

def row_add(request):
    data = json.loads(request.body)
    print(data)
    model_name = data.pop('model_name')
    for model in apps.get_models():
        if model._meta.verbose_name_plural == model_name:
            cur_model = model
            break
    print(data)
    try:
        cur_obj = cur_model.objects.create(**data)
        cur_obj.full_clean()
        cur_obj.save()
    except Exception as e:
        print(str(e))
        return JsonResponse({"Ошибка"}, status=500)
    return JsonResponse({},status=200)