from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login_success/', views.login_success, name='login_success'),
#     path('zawody/<int:pk>', views.zawody_aktywne, name='zawody_aktywne'),
    path('szczegoly/<int:pk>', views.zawody_aktywne_detail, name='zawody_aktywne_detail'),
    path('rozgrywane/<int:pk>', views.zawody_rozgrywane_detail, name='zawody_rozgrywane_detail'),
    path('propozycje/<slug:pk>', views.zawody_aktywne_propozycje, name='zawody_aktywne_propozycje'),
    path('przepisy', views.przepisy, name='przepisy'),
    path('przepisy/<slug:pk>/',views.przepisy_detail, name='przepisy_detail'),
    path('programy', views.programy, name='programy'),
    path('programy/<slug:pk>/',views.programy_detail, name='programy_detail'),
    path('artykuly', views.artykuly, name='artukuly'),
    path('zawodnicy', views.zawodnicy_index, name='zawodnicy_index'),
    path('zawodnik', views.zawodnik_dane, name='zawodnik_dane'),
    path('kluby', views.kluby_index, name='kluby_index'),
    path('404', views.str_404, name='str_404')
]
