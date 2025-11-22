from django.contrib import admin
from .models import Colaborador, EPIEntrega

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'matricula', 'cargo', 'setor', 'tamanho', 'ativo', 'criado_em')
    search_fields = ('nome', 'cpf', 'matricula', 'setor', 'cargo')
    list_filter = ('ativo', 'setor', 'cargo')


@admin.register(EPIEntrega)
class EPIEntregaAdmin(admin.ModelAdmin):
    list_display = ('nome_epi', 'colaborador', 'quantidade', 'data_entrega', 'validade', 'criado_em')
    search_fields = ('nome_epi', 'codigo_epi', 'colaborador__nome', 'colaborador__cpf')
    list_filter = ('data_entrega',)
