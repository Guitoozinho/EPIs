from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
   path('colaboradores/adicionar/', views.adicionar_colaborador, name='adicionar_colaborador')
]

