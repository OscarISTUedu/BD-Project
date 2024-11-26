from django.shortcuts import render
from .models import Patient, Doctor, Neighborhood, Diagnosis, Visit, Ticket

def patient_list(request):
    patients = Patient.objects.all().values()
    fields = Patient._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': patients,'h1':Patient._meta.verbose_name_plural,'fields':fields})

def doctor_list(request):
    doctors = Doctor.objects.all().values()
    fields = Doctor._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': doctors, 'h1': Doctor._meta.verbose_name_plural, 'fields': fields})

def neighborhood_list(request):
    neighborhoods = Neighborhood.objects.all().values()
    fields = Neighborhood._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': neighborhoods, 'h1': Neighborhood._meta.verbose_name_plural, 'fields': fields})

def diagnoses_list(request):
    diagnoses = Diagnosis.objects.all().values()
    fields = Diagnosis._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': diagnoses, 'h1': Diagnosis._meta.verbose_name_plural, 'fields': fields})

def visit_list(request):
    visits = Visit.objects.all().values()
    fields = Visit._meta.get_fields()
    fields = fields[1:]
    return render(request, 'model_list.html',
                  {'models': visits, 'h1': Visit._meta.verbose_name_plural, 'fields': fields})

def ticket(request):
    tickets = Ticket.objects.all().values()
    fields = Ticket._meta.get_fields()
    return render(request, 'model_list.html',
                  {'models': tickets, 'h1': Ticket._meta.verbose_name_plural, 'fields': fields})