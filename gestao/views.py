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

    if 'oficina' in request.GET:
        oficina_id = request.GET.get('oficina')
        if oficina_id:
            oficina_selecionada = Oficina.objects.get(id=oficina_id)
            alunos = Aluno.objects.filter(oficinas=oficina_selecionada)

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

# --- Nossa API IoT (Corrigida e integrada ao banco) ---
@csrf_exempt
def registrar_presenca_iot(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            identificador = dados.get('identificador', '')

            try:
                # Busca o aluno pelo CPF
                aluno = Aluno.objects.get(cpf=identificador)
                
                # Busca a primeira oficina vinculada ao aluno para evitar o erro de IntegrityError
                oficina_padrao = aluno.oficinas.first() 
                
                if not oficina_padrao:
                    return JsonResponse({"status": "erro", "mensagem": "Aluno não matriculado em oficinas."}, status=400)

                # Cria a presença vinculada obrigatoriamente à oficina
                Presenca.objects.create(
                    aluno=aluno,
                    oficina=oficina_padrao,
                    data=date.today(),
                    presente=True
                )
                
                return JsonResponse({
                    "status": "sucesso", 
                    "mensagem": f"Presença registrada para {aluno.nome} na oficina {oficina_padrao.nome}!"
                })
            
            except Aluno.DoesNotExist:
                return JsonResponse({"status": "erro", "mensagem": "Aluno não encontrado."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"status": "erro", "mensagem": "Formato JSON inválido."}, status=400)
            
    return JsonResponse({"status": "erro", "mensagem": "Método não permitido."}, status=405)