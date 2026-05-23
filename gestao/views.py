from django.shortcuts import render, redirect
from django.views.generic import ListView
from datetime import date
from .models import Aluno, Oficina, Presenca

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# --- Nossa listagem antiga ---
class AlunoListView(ListView):
    model = Aluno
    template_name = 'gestao/lista_alunos.html'
    context_object_name = 'alunos'

# --- Nossa nova inteligência de chamada ---
def fazer_chamada(request):
    oficinas = Oficina.objects.all()
    oficina_selecionada = None
    alunos = []

    # Se o professor selecionou uma oficina no menu dropdown
    if 'oficina' in request.GET:
        oficina_id = request.GET.get('oficina')
        if oficina_id:
            oficina_selecionada = Oficina.objects.get(id=oficina_id)
            # Trazemos só os alunos matriculados nesta oficina
            alunos = Aluno.objects.filter(oficinas=oficina_selecionada)

    # Se o professor clicou em "Salvar Presenças"
    if request.method == 'POST':
        oficina_id = request.POST.get('oficina_id')
        data_aula = request.POST.get('data')
        # Pega a lista com os IDs de todos que tiveram a caixinha marcada
        alunos_presentes = request.POST.getlist('presentes') 
        
        oficina = Oficina.objects.get(id=oficina_id)
        alunos_da_oficina = Aluno.objects.filter(oficinas=oficina)

        # O sistema varre todos os alunos e salva no banco
        for aluno in alunos_da_oficina:
            # Se o ID do aluno estiver na lista dos marcados, presente = True
            presente = str(aluno.id) in alunos_presentes
            Presenca.objects.create(
                aluno=aluno,
                oficina=oficina,
                data=data_aula,
                presente=presente
            )
        # Após salvar, redireciona para a lista de alunos
        return redirect('lista_alunos')

    context = {
        'oficinas': oficinas,
        'oficina_selecionada': oficina_selecionada,
        'alunos': alunos,
        'hoje': date.today().strftime('%Y-%m-%d')
    }
    return render(request, 'gestao/fazer_chamada.html', context)



@csrf_exempt
def registrar_presenca_iot(request):
    """
    API invisível para receber dados do hardware (Simulador ou Celular NFC).
    """
    if request.method == 'POST':
        try:
            # Pega o pacote de dados que o hardware enviou
            dados = json.loads(request.body)
            identificador = dados.get('identificador', '')

            # Aqui você vê no terminal o que o hardware mandou
            print(f"BIP! O hardware enviou o ID: {identificador}")

            # Simulando o sucesso do registro
            return JsonResponse({"status": "sucesso", "mensagem": f"Presença registrada para o ID {identificador}!"})
            
        except json.JSONDecodeError:
            return JsonResponse({"status": "erro", "mensagem": "Formato de dados inválido."}, status=400)
            
    return JsonResponse({"status": "erro", "mensagem": "Apenas requisições POST são aceitas."}, status=405)