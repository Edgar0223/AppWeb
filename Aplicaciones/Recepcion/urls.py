from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('inicioR/',views.inicioR,name='inicioR'),
    path('inicioRececpcion/',views.inicioRececpcion,name='inicioRececpcion'),

    path('almAli2/',views.almAli2,name='almAli2'),
    path('almAlf2/',views.almAlf2,name='almAlf2'),
    path('almFri2/',views.almFri2,name='almFri2'),
    path('almPT2/',views.almPT2,name='almPT2'),
    path('verCon2/',views.verCon2,name='verCon2'),
    path('op123/',views.op123,name='op123'),
    path('tras2/',views.tras2,name='tras2'),
    path('coPro2/',views.coPro2,name='coPro2'),
    path('m2/',views.m2,name='m2'),







]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
