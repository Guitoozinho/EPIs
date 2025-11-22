from django.urls import path
from . import views

app_name = 'controle_epis'

urlpatterns = [
    path('', views.home, name='home'),
    path('colaboradores/', views.lista_colaboradores, name='lista_colaboradores'),
    path('colaboradores/cadastrar/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('epis/cadastrar/', views.cadastrar_epi, name='cadastrar_epi'),
    path('entregas/registrar/', views.registrar_entrega, name='registrar_entrega'),
    path('sucesso/<str:tipo>/<int:pk>/', views.sucesso, name='sucesso'),

    # API route (mantém a rota que eu dei no HTML exemplo)
    path('api/colaboradores/adicionar/', views.adicionar_colaborador_api, name='adicionar_colaborador_api'),
]
