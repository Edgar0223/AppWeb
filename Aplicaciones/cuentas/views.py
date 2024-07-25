from django.shortcuts import render, redirect, get_object_or_404
from .models import contabilidad, empresas, pagos, catalogoEmp
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
from Aplicaciones.Trabajo.models import Nota, Usuario, proveedores, pagosProv ,fruta, lavado, congelado, quebrado, concervacion
from django.conf import settings
from datetime import date
from django.db.models import Q
import json
import logging
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)
# Create your views here.


def home2(request):
    user = Usuario.objects.all()
    return render(request, 'finanzas.html',{'user':user})
@user_passes_test(is_admin, login_url='/error/' )
def inicioFin(request):
    # Obtener saldos totales
    saldo_total_empresas = empresas.objects.aggregate(saldo_total=Sum('saldo'))['saldo_total'] or 0
    saldo_total_proveedores = proveedores.objects.aggregate(saldo_total=Sum('saldo'))['saldo_total'] or 0
    saldo_concentrado = saldo_total_empresas + saldo_total_proveedores

    # Contar los registros
    total_empresas = empresas.objects.count()
    total_proveedores = proveedores.objects.count()
    total_registros = total_empresas + total_proveedores

    # Obtener totales de contabilidad y Nota
    contabilidad_total = contabilidad.objects.aggregate(contabilidad_total=Sum('total'))['contabilidad_total'] or 0
    Nota_total = Nota.objects.aggregate(Nota_total=Sum('totalP'))['Nota_total'] or 0

    # Datos para gráficos
    pagos_empresas = list(pagos.objects.values('fechaPago').annotate(total=Sum('total')).order_by('fechaPago'))
    pagos_proveedores = list(pagosProv.objects.values('fechaPago').annotate(total=Sum('total')).order_by('fechaPago'))

    # Log para verificar los datos
    logger.debug(f"Pagos Empresas: {pagos_empresas}")
    logger.debug(f"Pagos Proveedores: {pagos_proveedores}")

    # Serializar datos a JSON
    pagos_empresas_json = json.dumps(pagos_empresas, default=str)
    pagos_proveedores_json = json.dumps(pagos_proveedores, default=str)

    return render(request, 'inicioFin.html', {
        'saldo_concentrado': saldo_concentrado,
        'total_registros': total_registros,
        'contabilidad_total': contabilidad_total,
        'Nota_total': Nota_total,
        'pagos_empresas': pagos_empresas_json,
        'pagos_proveedores': pagos_proveedores_json
    })
def terminos(request):
    return render(request, 'terminos.html')
def politicas(request):
    return render(request, 'politicas.html')
#------------------------CONTABILODAD---------------------------------------
@user_passes_test(is_admin, login_url='/error/' )
def conta(request):
    cat = catalogoEmp.objects.all()
    e = empresas.objects.all()
    saldo_total = e.aggregate(saldo_total=Sum('saldo'))['saldo_total']
    numero_facturas_vencidas = contabilidad.objects.filter(vencido=True).count()

    # Crear una lista para almacenar las empresas junto con su última fecha de pago
    empresas_con_ultimos_pagos = []
    
    for empresa in e:
        ultimo_pago = pagos.objects.filter(nombre=empresa).order_by('-fechaPago').first()
        ultima_fecha_pago = ultimo_pago.fechaPago if ultimo_pago else None
        empresas_con_ultimos_pagos.append({
            'empresa': empresa,
            'ultima_fecha_pago': ultima_fecha_pago
        })

    return render(request, 'conta.html', {
        'empresas_con_ultimos_pagos': empresas_con_ultimos_pagos,
        'saldo_total': saldo_total,
        'cat': cat,
        'numero_facturas_vencidas': numero_facturas_vencidas
    })
@require_http_methods(["DELETE"])
def eliminarConta(request, emp_id):
    try:
        factura = empresas.objects.get(id=emp_id)
        factura.delete()
        messages.success(request, 'Factura eliminada y saldo actualizado!')
        return JsonResponse({'success': True})
    except empresas.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Factura no encontrada.'})
@user_passes_test(is_admin, login_url='/error/' )
def conta2(request):
    cat = catalogoEmp.objects.all()
    e = empresas.objects.all()
    return render(request, 'conta.html', {'empresa':e,'cat':cat})

def facturas(request):
    actualizar_vencimiento()
    con_list = contabilidad.objects.all()
    # Asegúrate de actualizar los registros antes de obtener los vencidos
    return render(request, 'fac2.html', {'con': con_list})
@user_passes_test(is_admin, login_url='/error/')
def agregarEmp(request):
    cat = catalogoEmp.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rfc = request.POST.get('rfc')
        banco = request.POST.get('banco')
        cuenta = request.POST.get('cuenta')
        dias_vencimiento = request.POST.get('dias_vencimiento')
        tipo = request.POST.get('tipo')
        isr_aplicable = request.POST.get('isr_aplicable') == 'on'  # Nuevo campo para ISR
        retencion_iva_aplicable = request.POST.get('retencion_iva_aplicable') == 'on'  # Nuevo campo para retención de IVA
        tipo = catalogoEmp.objects.get(id=tipo)
        saldo = 0
        e = empresas.objects.create(
            nombre=nombre,
            rfc=rfc,
            banco=banco,
            cuenta=cuenta,
            tipo=tipo,
            saldo=saldo,
            dias_vencimiento=dias_vencimiento,
            isr_aplicable=isr_aplicable,
            retencion_iva_aplicable=retencion_iva_aplicable
        )
        messages.success(request, 'Guardado!!')
        return redirect('/conta')
    return render(request, 'conta.html', {'cat': cat})
@user_passes_test(is_admin, login_url='/error/')
def editarEmp(request,empresa_id):
    cat = empresas.objects.get(id = empresa_id)
    cat2 = catalogoEmp.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rfc = request.POST.get('rfc')
        banco = request.POST.get('banco')
        cuenta = request.POST.get('cuenta')
        dias_vencimiento = request.POST.get('dias_vencimiento')
        tipo = request.POST.get('tipo')
        isr_aplicable = request.POST.get('isr_aplicable') == 'on'  # Nuevo campo para ISR
        retencion_iva_aplicable = request.POST.get('retencion_iva_aplicable') == 'on'  # Nuevo campo para retención de IVA
        tipo = catalogoEmp.objects.get(id=tipo)
        saldo = request.POST.get('saldo')

        cat.nombre = nombre
        cat.rfc = rfc
        cat.banco = banco
        cat.nombre = cuenta
        cat.dias_vencimiento = dias_vencimiento
        cat.tipo = tipo
        cat.isr_aplicable = isr_aplicable
        cat.retencion_iva_aplicable = retencion_iva_aplicable
        cat.saldo = saldo

        cat.save()
        messages.success(request, 'Guardado!!')
        return redirect('/conta')
    return render(request, 'ediConta.html', {'cat': cat,'cat2': cat2})

@user_passes_test(is_admin, login_url='/error/' )
def infoProv(request,prov_id):
    actualizar_vencimiento()
    prov = empresas.objects.get(id=prov_id)
    con = contabilidad.objects.filter(nombre = prov).order_by('-id')
    # Asegúrate de actualizar los registros antes de obtener los vencidos
    detalles_con = []  # lista para almacenar detalles de contabilidad junto con fechas y días faltantes
    hoy = date.today()
    
    for registro in con:
        fecha_pago = registro.fecha + timedelta(days=prov.dias_vencimiento)
        dias_faltantes = (fecha_pago - hoy).days
        detalles_con.append({
            'registro': registro,
            'fecha_pago': fecha_pago,
            'dias_faltantes': dias_faltantes
        })
    
    return render(request, 'proveedor.html', {'prov': prov, 'detalles_con': detalles_con})
@user_passes_test(is_admin, login_url='/error/' )
def agregarFacturas(request):
    con = contabilidad.objects.all()
    pag = pagos.objects.all()
    emp = empresas.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        noFac = request.POST.get('noFac')
        folioF = request.POST.get('folioF')
        fecha = request.POST.get('fecha')
        concepto = request.POST.get('concepto')
        monto = Decimal(request.POST.get('monto'))
        
        iva = monto * Decimal(0.16)
        nombre_empresa = empresas.objects.get(id=nombre)

        if nombre_empresa.isr_aplicable:
            isr = (monto * Decimal(1.25))/Decimal(100)  # Supongamos que el ISR es del 10%
            retencion = isr
        
        elif nombre_empresa.retencion_iva_aplicable:
            retencion_iva = iva * Decimal(0.25)  # Supongamos que la retención de IVA es del 10%
            retencion = retencion_iva
        else:
            retencion = 0
        total = monto + iva - retencion

        # Depuración: imprimir los registros de contabilidad para esta empresa
        registros_contabilidad = contabilidad.objects.filter(nombre=nombre_empresa)
        print(f"Registros en contabilidad para esta empresa ({nombre_empresa}): {registros_contabilidad}")

        # Calcular la suma manualmente si es necesario
        total_sum = sum(registro.total for registro in registros_contabilidad)

        # Depuración: imprimir el total sumado
        print(f"Total sum para la empresa {nombre_empresa}: {total_sum}")

        con = contabilidad.objects.create(
            nombre=nombre_empresa,
            noFac=noFac,
            folioF=folioF,
            fecha=fecha,
            concepto=concepto,
            monto=monto,
            iva=iva,
            total=total,
            retencion=retencion
        )
        con.save()
        messages.success(request, 'Guardado!')
        return redirect('/agregarFacturas')
    return render(request, 'fac.html', {'emp': emp})

@user_passes_test(is_admin, login_url='/error/' )
def pago1(request):
    emp = empresas.objects.all()
    con = contabilidad.objects.filter(en_pago=False)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        total = Decimal(request.POST.get('total'))
        fechaPago = request.POST.get('fechaPago')
        refe = request.POST.get('refe')
        formaPago = request.POST.get('formaPago')
        nombre = empresas.objects.get(id=nombre)
        movimientos_seleccionados = request.POST.getlist('movimientos_seleccionados')

        # Crear registro de pago
        pago = pagos.objects.create(
            nombre=nombre,
            total=total,
            fechaPago=fechaPago,
            refe=refe,
            formaPago=formaPago,
            movi=','.join(movimientos_seleccionados),
        )
        pago.save()

        # Procesar los movimientos seleccionados
        frutas_seleccionadas = contabilidad.objects.filter(noFac__in=movimientos_seleccionados)
        for fruta in frutas_seleccionadas:
            if total <= 0:
                break

            if fruta.total > total:
                fruta.total -= total
                fruta.pago = pago  # Asignar el pago al movimiento
                fruta.save()
                total = 0
            else:
                total -= fruta.total
                fruta.total = 0
                fruta.en_pago = True
                fruta.pago = pago  # Asignar el pago al movimiento
                fruta.save()

        messages.success(request, 'Guardado!')
        return redirect('/pago1')
    return render(request, 'pago.html', {'emp': emp, 'con': con})


@user_passes_test(is_admin, login_url='/error/' )
def eliminarFactura(request, factura_id):
    factura = contabilidad.objects.get(id=factura_id)
    empresa = factura.nombre

    # Restar el total del registro al saldo de la empresa
    if empresa.saldo is not None:
        empresa.saldo -= factura.total
        empresa.save()

    factura.delete()
    messages.success(request, 'Factura eliminada y saldo actualizado!')
    return redirect('/conta')
@user_passes_test(is_admin, login_url='/error/' )
def eliminarPago(request, pago_id):
    factura = pagos.objects.get(id=pago_id)
    empresa = factura.nombre

    # Restar el total del registro al saldo de la empresa
    if empresa.saldo is not None:
        empresa.saldo += factura.total
        empresa.save()

    # Actualizar los registros de contabilidad asociados con este pago
    registros_contabilidad = contabilidad.objects.filter(pago=factura)
    registros_contabilidad.update(en_pago=False, pago=None)

    factura.delete()
    messages.success(request, 'Factura eliminada y saldo actualizado!')
    return redirect('/pagos2')
@user_passes_test(is_admin, login_url='/error/' )
def verPagos(request, empresa_id):
    # Obtener la empresa específica
    empresa = get_object_or_404(empresas, id=empresa_id)
    
    # Obtener solo los pagos correspondientes a esa empresa
    con = pagos.objects.filter(nombre=empresa)
    
    context = {
        'con': con,
        'empresa': empresa,
    }

    return render(request, 'pagos.html', context)
@user_passes_test(is_admin, login_url='/error/' )
def ven(request):
    con = contabilidad.objects.filter(vencido=True, en_pago=False)
    today = datetime.today().date()
    detalles_vencimiento = []
    # Asegúrate de actualizar los registros antes de obtener los vencidos
    actualizar_vencimiento()
    for registro in con:
        fecha_registro = registro.fecha
        empresa = registro.nombre
        dias_vencimiento = empresa.dias_vencimiento if empresa.dias_vencimiento is not None else 15
        dias_diferencia = (today - fecha_registro).days - dias_vencimiento

        detalles_vencimiento.append({
            'registro': registro,
            'dias_diferencia': dias_diferencia
        })

    return render(request, 'resumen_facturas_vencidas.html', {'detalles_vencimiento': detalles_vencimiento})
@user_passes_test(is_admin, login_url='/error/' )
def pagos2(request):
    pag = pagos.objects.all()
    return render(request, 'pagos2.html', {'con':pag})
#--------reporte------------------------------------------------------------------------------
def generar_reporte(request, empresa_id, start_date=None, end_date=None):
    empresa = get_object_or_404(empresas, id=empresa_id)

    # Obtener la fecha del primer registro de factura si start_date no se proporciona
    if start_date is None:
        primer_registro = contabilidad.objects.filter(nombre=empresa).order_by('fecha').first()
        if primer_registro:
            start_date = primer_registro.fecha
        else:
            start_date = date.today()  # Si no hay facturas, usa la fecha actual
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    
    if end_date is None:
        end_date = date.today()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    pagos_filtrados = pagos.objects.filter(nombre=empresa, fechaPago__range=[start_date, end_date])
    facturas_filtradas = contabilidad.objects.filter(nombre=empresa, fecha__range=[start_date, end_date])

    return render(request, 'reporte.html', {
        'empresa': empresa,
        'pagos_filtrados': pagos_filtrados,
        'facturas_filtradas': facturas_filtradas,
        'start_date': start_date,
        'end_date': end_date
    })



#---------------PROVEEDORES DE MATERIA PRIMA------------
def materiaPrima(request):
    prov = proveedores.objects.all()
    cat = catalogoEmp.objects.all()
    e = proveedores.objects.all()
    saldo_total = e.aggregate(saldo_total=Sum('saldo'))['saldo_total']
    numero_facturas_vencidas = Nota.objects.filter(vencido=True).count()

    # Crear una lista para almacenar las empresas junto con su última fecha de pago
    empresas_con_ultimos_pagos = []
    
    for empresa in e:
        ultimo_pago = pagosProv.objects.filter(nombre=empresa).order_by('-fechaPago').first()
        ultima_fecha_pago = ultimo_pago.fechaPago if ultimo_pago else None
        empresas_con_ultimos_pagos.append({
            'empresa': empresa,
            'ultima_fecha_pago': ultima_fecha_pago
        })

    return render(request, 'agri.html', {
        'empresas_con_ultimos_pagos': empresas_con_ultimos_pagos,
        'saldo_total': saldo_total,
        'cat': cat,
        'prov': prov,
        'numero_facturas_vencidas': numero_facturas_vencidas
    })
def eliminarProv(request, emp_id):
    factura = proveedores.objects.get(id=emp_id)
    factura.delete()
    messages.success(request, 'Factura eliminada y saldo actualizado!')
    return redirect('/materiaPrima')      
def agregarAgri(request):
    cat = catalogoEmp.objects.all()
    prov = proveedores.objects.all()
    e = proveedores.objects.all()
    saldo_total = e.aggregate(saldo_total=Sum('saldo'))['saldo_total']
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        saldo = Decimal(request.POST.get('saldo'))
        dias_vencimiento = request.POST.get('dias_vencimiento')
        saldo_cajas = request.POST.get('saldo_cajas')
        tipo = request.POST.get('tipo')

        tipo = catalogoEmp.objects.get(id = tipo)
        agricultor = proveedores.objects.create(
            nombre=nombre,
            saldo=saldo,
            dias_vencimiento=dias_vencimiento,
            saldo_cajas=saldo_cajas,
            tipo=tipo
        )


        agricultor.save()
        messages.success(request, 'Guardado!')
        return redirect('/agregarAgri')
    return render ( request, 'agri.html', {'cat':cat,'prov':prov,'saldo_total':saldo_total})


def infoAgri(request,agri_id):
    actualizar_vencimiento_prov()
    prov = proveedores.objects.get(id=agri_id)
    con = Nota.objects.filter(prov = prov)
    # Asegúrate de actualizar los registros antes de obtener los vencidos
    detalles_con = []  # lista para almacenar detalles de contabilidad junto con fechas y días faltantes
    hoy = date.today()
    for registro in con:
        totalK2 = registro.kilosN - registro.totalK
        fecha_pago = registro.fecha + timedelta(days=prov.dias_vencimiento)
        dias_faltantes = (fecha_pago - hoy).days
        detalles_con.append({
            'registro': registro,
            'fecha_pago': fecha_pago,
            'dias_faltantes': dias_faltantes,
            'totalK':totalK2
        })
    
    return render(request, 'agricultor.html', {'prov': prov, 'detalles_con': detalles_con})

@user_passes_test(is_admin, login_url='/error/' )
def eliminarNota(request, agri_id):
    factura = get_object_or_404(Nota, folio=agri_id)  # Ajuste aquí
    proveedor = factura.prov  # Ajuste aquí

    # Restar el total del registro al saldo del proveedor
    if proveedor.saldo is not None:
        proveedor.saldo -= factura.totalP  # Asegúrate de restar el campo correcto
        proveedor.save()

    factura.delete()
    messages.success(request, 'Factura eliminada y saldo actualizado!')
    return redirect('/materiaPrima')

def facturasProv(request):
    actualizar_vencimiento_prov()
    con_list = Nota.objects.all()
    # Asegúrate de actualizar los registros antes de obtener los vencidos
    return render(request, 'facProv.html', {'con': con_list})
@user_passes_test(is_admin, login_url='/error/' )
def venProv(request):
    actualizar_vencimiento_prov()
    con = Nota.objects.filter(vencido=True, en_pago=False)
    today = datetime.today().date()
    detalles_vencimiento = []

    for registro in con:
        fecha_registro = registro.fecha
        empresa = registro.nombre  # Asegúrate de que `nombre` sea una relación ForeignKey a `Empresa`
        
        if isinstance(empresa, empresas):
            dias_vencimiento = empresa.dias_vencimiento if empresa.dias_vencimiento is not None else 15
            
            # Calcula la fecha de pago sumando los días de vencimiento a la fecha de registro
            fecha_pago = fecha_registro + timedelta(days=dias_vencimiento)
            
            # Calcula los días de diferencia entre la fecha de hoy y la fecha de pago
            dias_diferencia = (fecha_pago - today).days
            
            detalles_vencimiento.append({
                'registro': registro,
                'dias_diferencia': dias_diferencia,
                'fecha_pago': fecha_pago
            })
        else:
            # Manejo de error si `empresa` no es del tipo esperado
            detalles_vencimiento.append({
                'registro': registro,
                'dias_diferencia': None,
                'fecha_pago': None,
                'error': 'Empresa no válida'
            })

    return render(request, 'resumen_facturas_vencidas_prov.html', {'detalles_vencimiento': detalles_vencimiento})


def pagoProv1(request):
    emp = proveedores.objects.all()
    con = Nota.objects.filter(en_pago=False)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        total = Decimal(request.POST.get('total'))
        fechaPago = request.POST.get('fechaPago')
        refe = request.POST.get('refe')
        formaPago = request.POST.get('formaPago')
        nombre = proveedores.objects.get(id=nombre)
        # Depuración: imprimir los registros de contabilidad para esta empresa
        registros_contabilidad = Nota.objects.filter(nombre=nombre)
        print(f"Registros en contabilidad para esta empresa ({nombre}): {registros_contabilidad}")

        # Calcular la suma manualmente si es necesario
        total_sum = sum(registro.total for registro in registros_contabilidad)

        # Depuración: imprimir el total sumado
        print(f"Total sum para la empresa {nombre}: {total_sum}")
        movimientos_seleccionados = request.POST.getlist('movimientos_seleccionados')


        # Convertir los valores a enteros
        movi = movimientos_seleccionados
   
        con = pagosProv.objects.create(
            nombre=nombre,
            total=total,
            fechaPago=fechaPago,
            refe=refe,
            formaPago=formaPago,
            movi=','.join(movi) ,
        )
        con.save()
        
        # Convertir los movimientos a objetos Movimiento
        frutas_seleccionadas = Nota.objects.filter(folio__in=movimientos_seleccionados)
        frutas_seleccionadas.update(en_pago=True, pago=con)
        messages.success(request, 'Guardado!')
        return redirect('/pagoProv1')
    return render ( request, 'pagoProv.html', {'emp':emp, 'con':con})

@user_passes_test(is_admin, login_url='/error/' )
def eliminarPagoProv(request, pago_id):
    factura = pagosProv.objects.get(id=pago_id)
    empresa = factura.nombre

    # Restar el total del registro al saldo de la empresa
    if empresa.saldo is not None:
        empresa.saldo += factura.total
        empresa.save()

    # Actualizar los registros de contabilidad asociados con este pago
    registros_contabilidad = Nota.objects.filter(pago=factura)
    registros_contabilidad.update(en_pago=False, pago=None)

    factura.delete()
    messages.success(request, 'Factura eliminada y saldo actualizado!')
    return redirect('/pagos2')

@user_passes_test(is_admin, login_url='/error/' )
def verPagosProv1(request, empresa_id):
    # Obtener la empresa específica
    empresa = get_object_or_404(proveedores, id=empresa_id)
    
    # Obtener solo los pagos correspondientes a esa empresa
    con = pagosProv.objects.filter(nombre=empresa)
    
    context = {
        'con': con,
        'empresa': empresa,
    }

    return render(request, 'pagosProv.html', context)


@user_passes_test(is_admin, login_url='/error/' )
def pagosProv2(request):
    pag = pagosProv.objects.all()
    return render(request, 'pagosProv2.html', {'con':pag})


















#-----------------------------------------------------------------METODOS DE PROCESOS-------------------------------------------------------
def actualizar_vencimiento():
    today = datetime.today().date()
    registros = contabilidad.objects.all()

    for registro in registros:
        empresa = registro.nombre  # Asumiendo que 'nombre' es una relación ForeignKey a la empresa
        dias_vencimiento = empresa.dias_vencimiento if empresa.dias_vencimiento is not None else 15
        dias_diferencia = (today - registro.fecha).days

        if dias_diferencia > dias_vencimiento:
            registro.vencido = True
        else:
            registro.vencido = False
        registro.save()
def actualizar_vencimiento_prov():
    today = datetime.today().date()
    registros = Nota.objects.all()

    for registro in registros:
        proveedor = registro.prov  # Asumiendo que 'prov' es la relación ForeignKey a proveedores en Nota
        dias_vencimiento = proveedor.dias_vencimiento if proveedor.dias_vencimiento is not None else 15
        dias_diferencia = (today - registro.fecha).days

        if dias_diferencia > dias_vencimiento:
            registro.vencido = True
        else:
            registro.vencido = False
        registro.save()

def recalculate_saldos():
    # Restablece el saldo de todas las empresas a cero
    empresas2 = empresas.objects.all()
    for empresa in empresas2:
        empresa.saldo = 0
        empresa.save()

    # Suma los totales de contabilidad
    contabilidades = contabilidad.objects.all()
    for contabilidad2 in contabilidades:
        empresa = contabilidad2.nombre
        empresa.saldo += contabilidad2.total
        empresa.save()

    # Resta los totales de pagos
    pagos2 = pagos.objects.all()
    for pago in pagos2:
        empresa = pago.nombre
        empresa.saldo -= pago.total
        empresa.save()

    return HttpResponse("Saldos recalculados exitosamente")
def recalculate_saldos_prov():
    for proveedor in proveedores.objects.all():
        total_notas = Nota.objects.filter(prov=proveedor).aggregate(total=Sum('totalP'))['total'] or 0
        total_pagos = pagosProv.objects.filter(nombre=proveedor).aggregate(total=Sum('total'))['total'] or 0
        proveedor.saldo = total_notas - total_pagos
        proveedor.save()


#-------------------------------------------------------
def reporte_produccion(request):
    frutas = fruta.objects.all()

    detalles_lavado = []
    detalles_congelado = []
    detalles_quebrado = []
    detalles_conservacion = []

    for fruta_item in frutas:
        # Filtrar lavados relacionados con la fruta actual
        lavados = lavado.objects.filter(lote__fruta__nombre=fruta_item.nombre)
        for lavado_item in lavados:
            detalles_lavado.append({
                'fruta': fruta_item.nombre,
                'nombre_lavado': lavado_item.nombre.nombre,
                'kgNetos': lavado_item.kgNetos,
                'kg': lavado_item.kg,
                'horaEnvio': lavado_item.horaEnvio,
                'usuario': lavado_item.usuario.username,
                'estado': lavado_item.estado
            })

        # Filtrar congelados relacionados con la fruta actual
        congelados = congelado.objects.filter(lavado__lote__fruta__nombre=fruta_item.nombre)
        for congelado_item in congelados:
            detalles_congelado.append({
                'fruta': fruta_item.nombre,
                'nombre_congelado': congelado_item.nombre,
                'kgNetos': congelado_item.kgNetos,
                'kg': congelado_item.kg,
                'horaEnvio': congelado_item.horaEnvio,
                'usuario': congelado_item.usuario.username,
                'estado': congelado_item.estado
            })

        # Filtrar quebrados relacionados con la fruta actual
        quebrados = quebrado.objects.filter(congelado__lavado__lote__fruta__nombre=fruta_item.nombre)
        for quebrado_item in quebrados:
            detalles_quebrado.append({
                'fruta': fruta_item.nombre,
                'nombre_quebrado': quebrado_item.nombre,
                'kgNetos': quebrado_item.kgNetos,
                'kg': quebrado_item.kg,
                'horaEnvio': quebrado_item.horaEnvio,
                'usuario': quebrado_item.usuario.username,
                'estado': quebrado_item.estado
            })

        # Filtrar conservaciones relacionadas con la fruta actual
        conservaciones = conservacion.objects.filter(quebrado__congelado__lavado__lote__fruta__nombre=fruta_item.nombre)
        for conservacion_item in conservaciones:
            detalles_conservacion.append({
                'fruta': fruta_item.nombre,
                'nombre_conservacion': conservacion_item.nombre,
                'kgT': conservacion_item.kgT,
                'fecha': conservacion_item.fecha,
                'hora': conservacion_item.hora,
                'cliente': conservacion_item.cliente,
                'destino': conservacion_item.destino,
                'fecha_aceptacion': conservacion_item.fecha_aceptacion,
                'aceptador': conservacion_item.aceptador
            })

    context = {
        'detalles_lavado': detalles_lavado,
        'detalles_congelado': detalles_congelado,
        'detalles_quebrado': detalles_quebrado,
        'detalles_conservacion': detalles_conservacion
    }

    return render(request, 'reporte_produccion.html', context)