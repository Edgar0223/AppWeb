from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.intro, name='intro'),
    path('inicio/', views.inicio, name='inicio'),
    path('login_view/', views.login_view, name='login_view'),
    path('login/',views.login, name="login"),
    path('logout/', views.signout, name='logout'),
    path('i/', views.i, name='i'),
    path('ent/', views.ent, name='ent'),
    path('entrada/', views.entrada, name='entrada'),
    path('p/', views.p, name='p'),
    path('prov/', views.prov, name='prov'),
    path('p/eliminarProveedor/<fruta_id>/', views.eliminarProveedor, name='eliminarProveedor'),
    path('p/edicionProveedores/<prov_id>/', views.edicionProveedores, name='edicionProveedores'),
    path('eliminarTodo/', views.eliminarTodo, name='eliminarTodo'),
    path('ent/retorno/<fruta_id>/', views.retorno, name='retorno'),
    path('ent/', views.ent, name='ent'),
    path('error/', views.error, name='error'),
    path('verAl/', views.verAl, name='verAl'),
    path('home/', views.home, name='home'),
    path('banner/', views.banner, name='banner'),

    path('entEx/',views.entExt, name='entEx'),
    path('entEx/retornoEx/<fruta_id>/', views.retornoEx, name='retornoEx'),

    #maquila
    path('enviar/', views.enviar, name='enviar'),
    path('m/', views.m, name='m'),
    path('m/eliminarMaquila/<maquila_id>/', views.eliminarMaquila, name='eliminarMaquila'),
    path('m/edicionMaquila/<maquila_id>/', views.edicionMaquila, name='edicionMaquila'),


    #empleados
    path('registro/', views.registro,name= 'registro'),

    
    # conserva
    path('con/',views.con, name='con'),
    path('conserva/',views.conserva, name='conserva'),
    path('con/eliminarConserva/<conserva_id>/', views.eliminarConserva, name='eliminarConserva'),
    path('con/edicionConserva/<conserva_id>/', views.edicionConserva, name='edicionConserva'),
    path('aceptar_rechazar_conserva/<conserva_id>/', views.aceptar_rechazar_conserva, name='aceptar_rechazar_conserva'),



    #almacen
    path('registrarFruta/', views.registrarFruta, name='registrarFruta'),
    path('op/', views.op, name='op'),
    path('op/edicionFruta/<fruta_id>/', views.edicionFruta, name='edicionFruta'),
    path('op/eliminarFruta/<fruta_id>/', views.eliminarFruta, name='eliminarFruta'),
    path('vent/', views.vent, name='vent'),

    #registro de fresa a despate
    path('registrarDespate/', views.registrarDespate, name='registrarDespate'),
    path('op2/', views.op2, name='op2'),
    path('op2/edicionDespate/<fruta_id>/', views.edicionDespate, name='edicionDespate'),
    path('op2/eliminarDespate/<fruta_id>/', views.eliminarDespate, name='eliminarDespate'),
    
    #registro de despate a lavado
    path('registrarLavado/', views.registrarLavado, name='registrarLavado'),
    path('op3/', views.op3, name='op3'),
    path('op3/edicionLavado/<fruta_id>/', views.edicionLavado, name='edicionLavado'),
    path('op3/eliminarLavado/<fruta_id>/', views.eliminarLavado, name='eliminarLavado'),

    
    #registro de lavado a congelado
    path('registrarCongelado/', views.registrarCongelado, name='registrarCongelado'),
    path('op4/', views.op4, name='op4'),
    path('op4/edicionCongelado/<fruta_id>/', views.edicionCongelado, name='edicionCongelado'),
    path('op4/eliminarCongelado/<fruta_id>/', views.eliminarCongelado, name='eliminarCongelado'),


    #registro de congelado a quebrado
    path('registrarQuebrado/', views.registrarQuebrado, name='registrarQuebrado'),
    path('op5/', views.op5, name='op5'),
    path('op5/edicionQuebrado/<fruta_id>/', views.edicionQuebrado, name='edicionQuebrado'),
    path('op5/eliminarQuebrado/<fruta_id>/', views.eliminarQuebrado, name='eliminarQuebrado'),


    #excel
    path('descargar_excel/<fruta_id>/', views.descargar_excel, name='descargar_excel'),
    path('descargar_excel2/<fruta_id>/', views.descargar_excel2, name='descargar_excel2'),
    path('descargar_excelPT/<fruta_id>/', views.descargar_excelPT, name='descargar_excelPT'),
    path('descargar_excelPT2/<fruta_id>/', views.descargar_excelPT2, name='descargar_excelPT2'),
    path('reporte/', views.reporte, name='reporte'),
    path('excelNota/<folio_id>', views.excelNota, name='excelNota'),
    path('crear_nota/', views.crear_nota, name='crear_nota'),

    #almacenes
    path('almAlf/', views.almAlf, name='almAlf'),
    path('almPT/', views.almPT, name='almPT'),
    path('almFri/', views.almFri, name='almFri'),
    path('almAli/', views.almAli, name='almAli'),
    path('verCon/', views.verCon, name='verCon'),
    path('tras/', views.tras, name='tras'),
    path('traspasarMovimiento/', views.traspasarMovimiento, name='traspasarMovimiento'),

    #ordenes
    path('aceptar_orden/<fruta_id>/', views.aceptar_orden, name='aceptar_orden'),
    path('orden/', views.orden, name='orden'),
    path('orden1/', views.orden1, name='orden1'),
    path('or1/', views.or1, name='or1'),
    path('orden1/eliminarOrden/<fruta_id>/', views.eliminarOrden, name='eliminarOrden'),
    path('orden1/edicionOrden/<fruta_id>/', views.edicionOrden, name='ordicionOrden'),



    #USuarios
    path('us/',views.us,name='us'),
    path('u/',views.u,name='u'),
    path('guardar_cambios/', views.guardar_cambios, name='guardar_cambios'),

    #compras
    path('compra/',views.compra, name='compra'),
    path('com/',views.com, name='com'),
    path('eliminarCompra/<fruta_id>/',views.eliminarCompra, name='eliminarCompra'),

    #rendimientos
    path('rend/',views.rend,name='rend'),

    #notas
    path('crear_nota/edicionNota/<nota_id>/', views.edicionNota, name='edicionNota'),
    

    #almacenes de Recepcion
    path('congeladoPro/',views.congeladoPro,name='congeladoPro'),
    path('coPro/',views.coPro,name='coPro'),
    path('coPro/eliminarCongeladoP/<fruta_id>/', views.eliminarCongeladoP, name='eliminarCongeladoP'),

    #cajas
    path('registrar_salida/',views.registrar_salida,name='registrar_salida'),

    #calidad
    path('muestreo/',views.muestreo,name='muestreo'),
    path('mues/',views.mues,name='mues'),
    path('mues2/',views.mues2,name='mues2'),
    path('mues2/edicionMuestreos/<mues_id>/',views.edicionMuestreos,name='edicionMuestreos'),
    path('mues2/eliminarMuestreos/<mues_id>/',views.eliminarMuestreos,name='eliminarMuestreos'),
    #-----fQuimicos
    path('kilosLiberados/',views.kilosLiberados,name='kilosLiberados'),
    path('kLib/',views.kLib,name='kLib'),
    path('imprimir/',views.imprimir,name='imprimir'),


    #catallogos
    path('embase/',views.embase,name='embase'),
    path('agregarEmbalaje/',views.agregarEmbalaje,name='agregarEmbalaje'),
    path('embase/edicionEmbalaje/<embalaje_id>/',views.edicionEmbalaje,name='edicionEmbalaje'),
    path('embase/eliminarEmbalaje/<embalaje_id>/',views.eliminarEmbalaje,name='eliminarEmbalaje'),

    path('palet/',views.palet,name='palet'),
    path('agregarPaleta/',views.agregarPaleta,name='agregarPaleta'),
    path('palet/edicionPaleta/<paleta_id>/',views.edicionPaleta,name='edicionPaleta'),
    path('palet/eliminarPaleta/<paleta_id>/',views.eliminarPaleta,name='eliminarPaleta'),

    path('nombres/',views.nombres,name='nombres'),
    path('agregarBerries/',views.agregarBerries,name='agregarBerries'),
    path('nombres/edicionBerries/<berries_id>/',views.edicionBerries,name='edicionBerries'),
    path('nombres/eliminarBerries/<berries_id>/',views.eliminarBerries,name='eliminarBerries'),

    
    path('registrarDevolucion/', views.registrarDevolucion, name='registrarDevolucion'),
    path('registrar_lavado/', views.registrar_lavado, name='registrar_lavado'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
