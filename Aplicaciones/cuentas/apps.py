from django.apps import AppConfig


class CuentasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Aplicaciones.cuentas'
    def ready(self):
        import Aplicaciones.cuentas.signals