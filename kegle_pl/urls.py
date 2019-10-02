from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('przepisy', views.przepisy, name='przepisy'),
    path('programy', views.programy, name='programy'),
    
]