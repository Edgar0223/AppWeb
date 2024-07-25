from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('terminos/',views.terminos,name='terminos'),
    path('politicas/',views.politicas,name='politicas'),
    path('reporte/<int:empresa_id>/', views.generar_reporte, name='generar_reporte'),
    path('reporte/<int:empresa_id>/<str:start_date>/<str:end_date>/', views.generar_reporte, name='generar_reporte_periodo'),
    
    #--------catalogo contable
    path('home2/',views.home2,name='home2'),
    path('inicioFin/',views.inicioFin,name='inicioFin'),
    path('conta/',views.conta,name='nombres'),
    path('eliminarConta/<emp_id>/',views.eliminarConta,name='eliminarConta'),
    path('agregarEmp/',views.agregarEmp,name='agregarEmp'),
    path('conta/infoProv/<prov_id>/',views.infoProv,name='infoProv'),
    path('conta/editarEmp/<int:empresa_id>/',views.editarEmp,name='editarEmp'),

    #----------catalogo de facturas
    path('agregarFacturas/',views.agregarFacturas,name='agregarFacturas'),
    path('facturas/',views.facturas,name='facturas'),
    path('pago1/',views.pago1,name='pago1'),
    path('eliminarFactura/<factura_id>/',views.eliminarFactura,name='eliminarFactura'),
    path('eliminarPago/<pago_id>/',views.eliminarPago,name='eliminarPago'),


    path('ven/', views.ven, name='ven'),
    path('pagos2/', views.pagos2, name='pagos2'),
    path('verPagos/<empresa_id>/', views.verPagos, name='verPagos'),
    path('verPagos/<pago_id>/', views.verPagos, name='verPagos'),

    #----------------PROVEEDORESD E MATERIA PRIMA   
    path('materiaPrima/', views.materiaPrima, name='materiaPrima'),
    path('agregarAgri/', views.agregarAgri, name='agregarAgri'),
    path('materiaPrima/infoAgri/<agri_id>/',views.infoAgri,name='infoAgri'),
    path('eliminarNota/<agri_id>/',views.eliminarNota,name='eliminarNota'),
    path('facturasProv/',views.facturasProv,name='facturasProv'),
    path('venProv/', views.venProv, name='venProv'),
    path('infoAgri/<agri_id>/', views.infoAgri, name='infoAgri'),
    path('pagoProv1', views.pagoProv1, name='pagoProv1'),
    path('eliminarPagoProv/<pago_id>/',views.eliminarPagoProv,name='eliminarPagoProv'),
    path('verPagosProv1/<empresa_id>/', views.verPagosProv1, name='verPagosProv1'),
    path('eliminarProv/<emp_id>/', views.eliminarProv, name='eliminarProv'),
    path('pagosProv2/', views.pagosProv2, name='pagosProv2'),




    #-----
    path('reporte_produccion/', views.reporte_produccion, name='reporte_produccion'),

    






]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
