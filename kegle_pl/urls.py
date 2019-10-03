from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('przepisy', views.przepisy, name='przepisy'),
    path('przepisy/<slug:pk>/',views.przepisy_detail, name='przepisy_detail'),
    path('programy', views.programy, name='programy'),
    path('programy/<slug:pk>/',views.programy_detail, name='programy_detail'),
]