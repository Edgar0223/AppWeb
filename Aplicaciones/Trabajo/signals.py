from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import *

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    user.usuario_activo = True
    user.capturando = True
    user.save()

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    user.usuario_activo = False
    user.capturando = False
    user.save()

@receiver(post_save, sender=fruta)
def update_saldo_cajas(sender, instance, created, **kwargs):
    if created:
        proveedor = instance.proveedor
        if proveedor.saldo_cajas is None:
            proveedor.saldo_cajas = 0
        proveedor.saldo_cajas += instance.unidades
        proveedor.save()