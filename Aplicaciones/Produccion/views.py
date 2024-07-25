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
@user_passes_test(is_admin_prod, login_url='/error/' )
def inicioProduccion(request):
    return render(request, 'produccion.html')
@user_passes_test(is_admin_prod, login_url='/error/' )
def produccion(request):
    return render(request, 'inicioProduccion.html')
@user_passes_test(is_admin_prod,login_url='/error/')
def op32(request):
    nom = materia.objects.all()
    emba = embalaje.objects.all()
    paletas = paleta.objects.all()
    frutas = lavado.objects.all().order_by('-id')
    fruta_obj = lavado.objects.order_by('-id').first()
    # Guardar el número de movimiento antes de eliminar la fruta
    return render(request, 'lavado2.html', {'Frutas': frutas,'nombre':nom,'emba':emba,'paletas':paletas})

@user_passes_test(is_admin_prod,login_url='/error/')
def op42(request):
    nom = materia.objects.all()
    emba = embalaje.objects.all()
    paletas = paleta.objects.all()
    frutas = congelado.objects.all().order_by('-id')
    fruta_obj = congelado.objects.order_by('-id').first()
    # Guardar el número de movimiento antes de eliminar la fruta
    ultimo_movimiento = fruta_obj.id
    frutas2 = congelado.objects.prefetch_related('quebrado_set').all().order_by('-id')
    return render(request, 'congelado2.html', {'Frutas': frutas,'frutas2':frutas2,'ultimo_movimiento':ultimo_movimiento,'nombre':nom,'emba':emba,'paletas':paletas})
@user_passes_test(is_admin_prod,login_url='/error/')
def op52(request):
    nom = materia.objects.all()
    emba = embalaje.objects.all()
    paletas = paleta.objects.all()
    frutas = quebrado.objects.all().order_by('-id')
    fruta_obj = quebrado.objects.order_by('-id').first()
    # Guardar el número de movimiento antes de eliminar la fruta
    ultimo_movimiento = fruta_obj.id
    return render(request, 'quebrado2.html', {'Frutas': frutas,'ultimo_movimiento':ultimo_movimiento,'nombre':nom,'emba':emba,'paletas':paletas})

@user_passes_test(is_admin_prod,login_url='/error/')
def con2(request):
    nom = materia.objects.all()
    emba = embalaje.objects.all()
    paletas = paleta.objects.all()
    frutas = concervacion.objects.all().order_by('-id')
    fruta_obj = concervacion.objects.order_by('-id').first()
    # Guardar el número de movimiento antes de eliminar la fruta
    ultimo_movimiento = fruta_obj.id
    return render(request, 'conserva2.html', {'Frutas': frutas,'ultimo_movimiento':ultimo_movimiento,'nombre':nom,'emba':emba,'paletas':paletas})

@user_passes_test(is_admin_prod,login_url='/error/')
def verAl2(request): 
    nombre_filtro = request.GET.get('nombre_filtro', '')  # Obtener el valor del parámetro GET
    frutas = fruta.objects.all().order_by('-movimiento')
    
    if nombre_filtro:
        frutas_filtradas = frutas.filter(nombre=nombre_filtro)
        total_cajas = frutas_filtradas.aggregate(total_cajas=Sum('unidades'))['total_cajas']
        total_kgNetos = frutas_filtradas.aggregate(total_kgNetos=Sum('kgNetos'))['total_kgNetos']
    else:
        total_cajas = 0
        total_kgNetos = 0

    context = {
        'Frutas': frutas,
        'total_cajas': total_cajas,
        'total_kgNetos': total_kgNetos,
        'nombre_filtro': nombre_filtro,  # Pasar el valor del filtro a la plantilla
    }

    return render(request, 'almacen2.html', context)
@user_passes_test(is_admin_prod, login_url='/error/' )
def or12(request):
    ordd= ordenes.objects.all()
    return render(request, 'orden22.html', {'Frutas': ordd})