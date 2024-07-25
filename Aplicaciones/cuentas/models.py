from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django import forms
from django.core.validators import MinValueValidator
# Create your models here.
class catalogoEmp(models.Model):
    nombre =  models.CharField(max_length=200, null=True)
    descripcion =  models.CharField(max_length=200, null=True)
class empresas(models.Model):
    nombre = models.CharField(max_length=100)
    rfc = models.CharField(max_length=13)
    banco = models.CharField(max_length=50,null=True)
    cuenta = models.CharField(max_length=20)
    tipo = models.ForeignKey(catalogoEmp, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    dias_vencimiento = models.IntegerField()
    isr_aplicable = models.BooleanField(default=False)  # Campo para indicar si aplica ISR
    retencion_iva_aplicable = models.BooleanField(default=False)  # Campo para indicar si aplica retención de IVA

class pagos(models.Model):
    nombre = models.ForeignKey(empresas, on_delete=models.CASCADE ,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    fechaPago = models.DateField()
    refe =  models.CharField(max_length=30, null=True)
    formaPago = models.CharField(max_length=30, null=True)
    movi = models.CharField(max_length=255, blank=True,null=True) 
class contabilidad(models.Model):
    nombre = models.ForeignKey(empresas, on_delete=models.CASCADE ,null=True)
    noFac = models.CharField(max_length=200, null=True)
    folioF = models.CharField(max_length=200, null=True)
    fecha = models.DateField()
    concepto = models.CharField(max_length=200, null=True)
    monto =  models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    iva =  models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    retencion =  models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)],null=True)
    total =  models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    vencido = models.BooleanField(default=False)
    en_pago = models.BooleanField(default=False)
    pago = models.ForeignKey(pagos, on_delete=models.SET_NULL, null=True, blank=True)


