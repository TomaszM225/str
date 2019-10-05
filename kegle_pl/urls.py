from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
#     path('zawody/<int:pk>', views.zawody_aktywne, name='zawody_aktywne'),
    path('szczegoly/<int:pk>', views.zawody_aktywne_detail, name='zawody_aktywne_detail'),
    path('rozgrywane/<int:pk>', views.zawody_rozgrywane_detail, name='zawody_rozgrywane_detail'),
    path('propozycje/<slug:pk>', views.zawody_aktywne_propozycje, name='zawody_aktywne_propozycje'),
    path('przepisy', views.przepisy, name='przepisy'),
    path('przepisy/<slug:pk>/',views.przepisy_detail, name='przepisy_detail'),
    path('programy', views.programy, name='programy'),
    path('programy/<slug:pk>/',views.programy_detail, name='programy_detail'),
]