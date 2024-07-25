from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('homeCalidad/',views.homeCalidad,name='homeCalidad'),
    path('inicioCa/',views.inicioCa,name='inicioCa'),


    path('mues3/',views.mues3,name='mues3'),
    path('mues4/',views.mues4,name='mues4'),
    path('kLib2/',views.kLib2,name='kLib2'),

    




]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
