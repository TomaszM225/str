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
    path('przepisy/<slug:pk>',views.przepisy_detail, name='przepisy_detail'),
    path('programy', views.programy, name='programy'),
    path('programy/<slug:pk>',views.programy_detail, name='programy_detail'),
    path('artykuly', views.artykuly, name='artukuly'),
    path('zawodnicy', views.zawodnicy_index, name='zawodnicy_index'),
    path('detale', views.zawodnik_dane, name='zawodnik_dane'),
    path('dodaj', views.zawodnik_dodaj, name='zawodnik_dodaj'),
    path('edit', views.zawodnik_edytuj, name='zawodnik_edytuj'),
    path('kluby', views.kluby_index, name='kluby_index'),
    path('konie', views.konie_index, name='konie_index'),
    path('kon/<int:pk>',views.kon_dane, name='kon_dane'),
    path('kon/zmiana/<int:pk>', views.kon_edit, name='kon_edit'),
    path('kon/dodaj', views.kon_dodaj, name='kon_dodaj'),
    path('zgloszenie/<int:pk>', views.zgloszenie_dodaj, name='zgloszenie_dodaj'),
    path('404', views.str_404, name='str_404')
]
