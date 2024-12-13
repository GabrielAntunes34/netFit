from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TreinoForm, SerieInlineFormSet
from .models import *

# Retorna a página inicial do site
def index(request):
    return  render(request, "netFitApp/index.html", {
        "mensagem": 'testando'
    })


# Retorna a página que lista os treinos do usuário
@login_required
def listar_treinos(request):
    treinos = Treino.objects.filter(usuario=request.user).prefetch_related('series__exercicio')
    return render(request, 'listarTreinos.html', {'treinos':treinos})


# Retorna a página enviar treino e lida com as requisições POST do seu formulário
@login_required
def montar_treino(request):
    if request.method == "POST":
        # Obtendo os dados de cada formulário da requisição
        treino_form = TreinoForm(request.POST)
        series_formset = SerieInlineFormSet(request.POST, instance=treino_form.instance)

        # Se a resposta é valida, Instanciamos o objeto
        if treino_form.is_valid() and series_form.is_valid():
            # Salvando o novo objeto de Treino no banco
            treino = treino_form.save(commit=False)
            treino.entusiasta = request.user
            treino.save()

            # Salvando a associação da chave estrageira na tabela séries
            series_formset.instance = treino
            series_formset.save()

            return redirect('listar_treinos')


    else:
        # Se não, a requisição é um get, e apenas respondemos com a página com os formulários
        treino_form = TreinoForm()
        series_form = SerieInlineFormSet()
    return render(request, 'criarTreino.html', {'treino_form':treino_form}, {'series_form':series_form})
