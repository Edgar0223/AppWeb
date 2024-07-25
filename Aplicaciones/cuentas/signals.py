from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import contabilidad, pagos, empresas
from Aplicaciones.Trabajo.models import Nota,pagosProv
from Aplicaciones.cuentas.views import  recalculate_saldos_prov

@receiver(post_save, sender=contabilidad)
def update_saldo_contabilidad(sender, instance, created, **kwargs):
    if created:
        empresa = instance.nombre
        empresa.saldo += instance.total
        empresa.save()

@receiver(post_save, sender=pagos)
def update_saldo_pagos(sender, instance, created, **kwargs):
    if created:
        empresa = instance.nombre
        empresa.saldo -= instance.total
        empresa.save()
@receiver(post_save, sender=Nota)
def update_saldo_nota(sender, instance, created, **kwargs):
    recalculate_saldos_prov()
    if created:
        proveedor = instance.prov
        proveedor.saldo += instance.totalP
        proveedor.save()
        recalculate_saldos_prov()

@receiver(post_save, sender=pagosProv)
def update_saldo_pagos_prov(sender, instance, created, **kwargs):
    recalculate_saldos_prov()
    if created:
        proveedor = instance.nombre
        proveedor.saldo -= instance.total
        proveedor.save()
        recalculate_saldos_prov()
