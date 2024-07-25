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
@user_passes_test(is_admin_cal, login_url='/error/' )
def homeCalidad(request):
    return render(request, 'Calidad.html')

@user_passes_test(is_admin_cal, login_url='/error/' )
def inicioCa(request):
    return render(request, 'inicioCalidad.html')
@user_passes_test(is_admin_cal, login_url='/error/' )
def mues3(request):
    frutas = recep.objects.all()
    prov = proveedores.objects.all()
    frut = materia.objects.all()
    return render(request, 'recepA.html', {'Frutas': frutas,'prov':prov,'frut':frut})
@user_passes_test(is_admin_cal, login_url='/error/' )
def mues4(request):
    frutas = recep.objects.all().order_by('-id')
    return render(request, 'recepB.html', {'Frutas': frutas})
@user_passes_test(is_admin_cal, login_url='/error/' )
def kLib2(request):
    fis = fisicoQ.objects.all().order_by('-id')
    producs = materia.objects.all()
    return render(request, 'fQuimicos2.html', {'fis':fis,'producs':producs})