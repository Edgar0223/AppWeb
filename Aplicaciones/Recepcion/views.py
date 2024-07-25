from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
import logging
from django.db.models import Sum,F, FloatField
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal,DivisionUndefined
from .utils import is_admin, is_admin_prod,is_admin_recep,is_admin_cal
from io import BytesIO
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import openpyxl
import datetime
from datetime import datetime ,timedelta,date,time
from openpyxl.styles import Protection, NamedStyle
from django.utils import timezone
from django.template.defaultfilters import default_if_none
from collections import defaultdict
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDictKeyError
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models.functions import TruncDate
from django.conf import settings
from Aplicaciones.Trabajo.models import *
# Create your views here.

@user_passes_test(is_admin_recep, login_url='/error/' )
def inicioRececpcion(request):
    return render(request, 'Recepcion.html')
@user_passes_test(is_admin_recep, login_url='/error/' )
def inicioR(request):
    return render(request, 'inicioRecepcion.html')
@user_passes_test(is_admin_recep, login_url='/error/' )
def almAli2(request):
    frutas = fruta.objects.all().order_by('-movimiento')
    return render(request, 'almacenAli2.html', {'Frutas': frutas})
@user_passes_test(is_admin_recep,login_url='/error/')
def almAlf2(request):
    frutas = alfrut.objects.all()
    return render(request, 'almacenAlf2.html', {'Frutas': frutas})
@user_passes_test(is_admin_recep,login_url='/error/')
def almFri2(request):
    frutas = frigoe.objects.all() 
    return render(request, 'almacenFri2.html', {'Frutas': frutas})
@user_passes_test(is_admin_recep,login_url='/error/')
def almPT2(request):
    nombre_filtro = request.GET.get('nombre_filtro', '')  # Obtener el valor del parámetro GET
    status = request.GET.get('status', '')  # Obtener el valor del parámetro GET
    frutas = concervacion.objects.all().order_by('-id')
    
    if nombre_filtro:
        frutas_filtradas = frutas.filter(nombre=nombre_filtro,destino=status)
        total_cajas = frutas_filtradas.aggregate(total_cajas=Sum('cajas'))['total_cajas']
        total_kgNetos = frutas_filtradas.aggregate(total_kgNetos=Sum('kgT'))['total_kgNetos']
    else:
        total_cajas = 0
        total_kgNetos = 0

    context = {
        'Frutas': frutas,
        'total_cajas': total_cajas,
        'total_kgNetos': total_kgNetos,
        'nombre_filtro': nombre_filtro,  # Pasar el valor del filtro a la plantilla
    }

    return render(request, 'almacenPT2.html', context)
@user_passes_test(is_admin_recep,login_url='/error/')
def verCon2(request):
    frutas = congelado.objects.all()
    return render(request, 'congeladoAlm2.html', {'Frutas': frutas})

@user_passes_test(is_admin_recep, login_url='/error/')
def op123(request):
    prov = proveedores.objects.all()
    ma = Maquila.objects.all().order_by('-id')
    nom = materia.objects.all()
    emba = embalaje.objects.all()
    paletas = paleta.objects.all()
    fruta_obj = fruta.objects.order_by('-movimiento').first()
    # Guardar el número de movimiento antes de eliminar la fruta
    ultimo_movimiento = fruta_obj.movimiento
    # Usar prefetch_related para obtener las relaciones de Maquila en una sola consulta
    frutas = fruta.objects.prefetch_related('maquila_set').all().order_by('-movimiento')
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        frutas = fruta.objects.filter(fecha__range=[fecha_inicio, fecha_fin]).order_by('-movimiento')
        return render(request, 'fruta123.html',{'Frutas': frutas, 'proveedores': prov, 'maq': ma,'nombre':nom,'emba':emba,'paletas':paletas,'ultimo_movimiento':ultimo_movimiento})
    else:
        frutas = fruta.objects.all().order_by('-movimiento')
        return render(request, 'fruta123.html', {'Frutas': frutas, 'proveedores': prov, 'maq': ma,'nombre':nom,'emba':emba,'paletas':paletas,'ultimo_movimiento':ultimo_movimiento})
    
    return render(request, 'fruta123.html', {'Frutas': frutas, 'proveedores': prov, 'maq': ma,'nombre':nom,'emba':emba,'paletas':paletas,'ultimo_movimiento':ultimo_movimiento})
@user_passes_test(is_admin_recep,login_url='/error/')
def tras2(request):
    return render(request, 'traspasos2.html')
@user_passes_test(is_admin_recep,login_url='/error/' )
def m2(request):
    frutas = Maquila.objects.all().order_by('-id')
    emba = embalaje.objects.all()
    paletas = paleta.objects.all()
    frut = materia.objects.all()

    return render(request, 'maquila2.html', {'Frutas': frutas,'emba':emba,'paletas':paletas,'frut':frut})
@user_passes_test(is_admin_prod, login_url='/error/' )
def coPro2(request):
    frutas = congeladoP.objects.all().order_by('-Con')
    nombre = materia.objects.all()
    return render(request, 'congeladoP2.html', {'Frutas': frutas,'nombre':nombre})