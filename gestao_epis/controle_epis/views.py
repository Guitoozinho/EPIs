from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Colaborador, EPIEntrega
from django.urls import reverse
from django.utils import timezone

def home(request):
    return render(request, 'controle_epis/home.html')


def lista_colaboradores(request):
    colaboradores = Colaborador.objects.all().order_by('nome')
    return render(request, 'controle_epis/lista_colaboradores.html', {'colaboradores': colaboradores})


def cadastrar_colaborador(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        cpf = request.POST.get('cpf', '').strip()
        matricula = request.POST.get('matricula')
        cargo = request.POST.get('cargo')
        setor = request.POST.get('setor')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        tamanho = request.POST.get('tamanho')

        if not nome or not cpf:
            return render(request, 'controle_epis/cadastrar_colaborador.html', {
                'error': 'Nome e CPF são obrigatórios.',
            })

        colaborador = Colaborador.objects.create(
            nome=nome, cpf=cpf, matricula=matricula or None, cargo=cargo or '', setor=setor or '',
            telefone=telefone or '', email=email or '', tamanho=tamanho or ''
        )
        return redirect('controle_epis:sucesso', tipo='colaborador', pk=colaborador.pk)

    return render(request, 'controle_epis/cadastrar_colaborador.html')


def cadastrar_epi(request):
    if request.method == 'POST':
        nome_epi = request.POST.get('nome_epi', '').strip()
        codigo_epi = request.POST.get('codigo_epi', '').strip()
        validade = request.POST.get('validade') or None

        if not nome_epi:
            return render(request, 'controle_epis/cadastrar_epi.html', {'error': 'Nome do EPI é obrigatório.'})

        # Isso cria um EPI "catálogo" se você quisesse; no A1 usamos entregas diretas,
        # então podemos apenas redirecionar ou armazenar em tabela separada. Para A1 mantemos o cadastro simples.
        # Aqui vamos apenas salvar uma entrega vazia como exemplo (ou redirecionar).
        return redirect('controle_epis:home')

    return render(request, 'controle_epis/cadastrar_epi.html')


def registrar_entrega(request):
    colaboradores = Colaborador.objects.all().order_by('nome')
    if request.method == 'POST':
        colaborador_id = request.POST.get('colaborador')
        nome_epi = request.POST.get('nome_epi', '').strip()
        codigo_epi = request.POST.get('codigo_epi', '').strip()
        data_entrega = request.POST.get('data_entrega') or timezone.now().date()
        validade = request.POST.get('validade') or None
        quantidade = request.POST.get('quantidade') or 1

        if not colaborador_id or not nome_epi:
            return render(request, 'controle_epis/registrar_entrega.html', {
                'colaboradores': colaboradores,
                'error': 'Colaborador e nome do EPI são obrigatórios.'
            })

        colaborador = get_object_or_404(Colaborador, pk=colaborador_id)
        entrega = EPIEntrega.objects.create(
            colaborador=colaborador,
            nome_epi=nome_epi,
            codigo_epi=codigo_epi or '',
            data_entrega=data_entrega,
            validade=validade if validade else None,
            quantidade=int(quantidade)
        )
        return redirect('controle_epis:sucesso', tipo='entrega', pk=entrega.pk)

    return render(request, 'controle_epis/registrar_entrega.html', {'colaboradores': colaboradores})


def sucesso(request, tipo, pk):
    # tipo: 'colaborador' ou 'entrega'
    contexto = {}
    if tipo == 'colaborador':
        contexto['obj'] = Colaborador.objects.filter(pk=pk).first()
    elif tipo == 'entrega':
        contexto['obj'] = EPIEntrega.objects.filter(pk=pk).first()
    contexto['tipo'] = tipo
    return render(request, 'controle_epis/sucesso.html', contexto)


# API compatível com JSON (mantém sua rota anterior)
@csrf_exempt
@require_POST
def adicionar_colaborador_api(request):
    try:
        if request.content_type == 'application/json':
            payload = json.loads(request.body.decode('utf-8') or '{}')
            nome = payload.get('nome')
            cpf = payload.get('cpf')
            matricula = payload.get('matricula')
            cargo = payload.get('cargo')
            setor = payload.get('setor')
            telefone = payload.get('telefone')
            email = payload.get('email')
            tamanho = payload.get('tamanho_uniforme') or payload.get('tamanho')

            # cria colaborador
            if not nome or not cpf:
                return JsonResponse({'error': 'Nome e CPF são obrigatórios.'}, status=400)

            colaborador = Colaborador.objects.create(
                nome=nome.strip(), cpf=cpf.strip(), matricula=matricula or None,
                cargo=cargo or '', setor=setor or '',
                telefone=telefone or '', email=email or '', tamanho=tamanho or ''
            )

            # se vier dados de EPI dentro do JSON, cria entrega também
            epi = payload.get('epi')
            if epi:
                EPIEntrega.objects.create(
                    colaborador=colaborador,
                    nome_epi=epi.get('nome_epi') or '',
                    codigo_epi=epi.get('codigo_epi') or '',
                    data_entrega=epi.get('data_entrega') or timezone.now().date(),
                    validade=epi.get('validade') or None,
                    quantidade=int(epi.get('quantidade') or 1)
                )

            return JsonResponse({'id': colaborador.id, 'message': 'Colaborador adicionado com sucesso!'}, status=201)

        return JsonResponse({'error': 'Tipo de conteúdo não suportado'}, status=415)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Erro interno', 'detail': str(e)}, status=500)
