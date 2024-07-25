from django.utils import timezone
from .models import contabilidad

def actualizar_estado_vencimiento():
    today = timezone.now().date()
    for factura in contabilidad.objects.all():
        dias_vencimiento = factura.dias_vencimiento if factura.dias_vencimiento is not None else 15
        dias_diferencia = (today - factura.fecha).days
        
        if dias_diferencia > dias_vencimiento:
            factura.vencido = True
            factura.save()

        else:
            factura.vencido = False
        
