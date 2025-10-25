from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Colaborador

# Create your views here.
def home(request):
    return render(request, 'controle_epis/home.html')

def adicionar_colaborador(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            colaborador = Colaborador(nome=nome)
            colaborador.save()
            return JsonResponse({'message': 'Colaborador adicionado com sucesso!'}, status=201)
        return JsonResponse({'error': 'Nome é obrigatório.'}, status=400)
    return JsonResponse({'error': 'Método não permitido.'}, status=405)