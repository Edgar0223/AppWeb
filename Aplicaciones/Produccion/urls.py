from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('produccion/',views.produccion,name='produccion'),
    path('inicioProduccion/',views.inicioProduccion,name='inicioProduccion'),



    path('op32/',views.op32,name='op32'),
    path('op42/',views.op42,name='op42'),
    path('op52/',views.op52,name='op52'),
    path('con2/',views.con2,name='con2'),
    path('verAl2/',views.verAl2,name='verAl2'),
    path('or12/',views.or12,name='or12'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
