from django.shortcuts import render, redirect
from django.views.generic import ListView
from datetime import date
from .models import Aluno, Oficina, Presenca

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# --- Nossa listagem de alunos ---
class AlunoListView(ListView):
    model = Aluno
    template_name = 'gestao/lista_alunos.html'
    context_object_name = 'alunos'

# --- Nossa inteligência de chamada manual ---
def fazer_chamada(request):
    oficinas = Oficina.objects.all()
    oficina_selecionada = None
    alunos = []

    # Se o professor selecionou uma oficina no menu dropdown
    if 'oficina' in request.GET:
        oficina_id = request.GET.get('oficina')
        if oficina_id:
            oficina_selecionada = Oficina.objects.get(id=oficina_id)
            alunos = Aluno.objects.filter(oficinas=oficina_selecionada)

    # Se o professor clicou em "Salvar Presenças"
    if request.method == 'POST':
        oficina_id = request.POST.get('oficina_id')
        data_aula = request.POST.get('data')
        alunos_presentes = request.POST.getlist('presentes') 
        
        oficina = Oficina.objects.get(id=oficina_id)
        alunos_da_oficina = Aluno.objects.filter(oficinas=oficina)

        for aluno in alunos_da_oficina:
            presente = str(aluno.id) in alunos_presentes
            Presenca.objects.create(
                aluno=aluno,
                oficina=oficina,
                data=data_aula,
                presente=presente
            )
        return redirect('lista_alunos')

    context = {
        'oficinas': oficinas,
        'oficina_selecionada': oficina_selecionada,
        'alunos': alunos,
        'hoje': date.today().strftime('%Y-%m-%d')
    }
    return render(request, 'gestao/fazer_chamada.html', context)

# --- Nossa API IoT (Integrada com o Banco de Dados) ---
@csrf_exempt
def registrar_presenca_iot(request):
    """
    API para receber o ID do cartão, buscar o aluno no banco e salvar a presença.
    """
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            identificador = dados.get('identificador', '')

            # Tenta encontrar o aluno pelo CPF (identificador)
            try:
                aluno = Aluno.objects.get(cpf=identificador)
                
                # Registra a presença no banco de dados com presente=True
                Presenca.objects.create(
                    aluno=aluno,
                    data=date.today(),
                    presente=True
                )
                
                return JsonResponse({
                    "status": "sucesso", 
                    "mensagem": f"Presença registrada para o aluno {aluno.nome}!"
                })
            
            except Aluno.DoesNotExist:
                return JsonResponse({"status": "erro", "mensagem": "Aluno não encontrado com este identificador."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"status": "erro", "mensagem": "Formato de dados inválido."}, status=400)
            
    return JsonResponse({"status": "erro", "mensagem": "Apenas requisições POST são aceitas."}, status=405)