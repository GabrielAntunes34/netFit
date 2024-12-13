from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TreinoForm, SerieInlineFormSet
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import *

# Retorna a página inicial do site
@login_required(login_url='/login')
def index(request):
    return render(request, "netFitApp/index.html", {
        "mensagem": 'testando'
    })

def login_view(request):
    if request.method == "POST":
        # recebe os atributos e loga
        username = request.POST['username']
        password = request.POST['senha']
        user = authenticate(request, username=username, password=password)

        # checa resultado
        if user is not None:
            login(request, user) # loga se tudo certo
            # redireciona para o caso de Uso
            return HttpResponseRedirect(reverse("index"))
        else:
            # se der errado, devolve erro
            return render(request, "netFitApp/login.html", {
                "msg_erro": "Username/senha inválidos"
            })
    else:
        # carrega pagina de login
        return render(request, "netFitApp/login.html")
    
def register(request):
    if request.method == "POST":
        # pega os atributos
        username = request.POST['username']
        cpf = request.POST['cpf']
        data = request.POST['data']
        password = request.POST['senha']
        password2 = request.POST['conf_senha']
        tipo = request.POST['tipo_usuario']

        # Verifica se as senhas coincidem
        if password != password2:
            return render(request, "netFitApp/register.html", {
                "msg_erro": "As senhas devem ser iguais."
            })

        # Cria o usuário principal
        try:
            user = Usuario.objects.create_user(
                username=username,
                password=password,
                cpf=cpf,
                data_nascimento=data,
            )
        except IntegrityError:
            return render(request, "netFitApp/register.html", {
                "msg_erro": "Já existe um usuário com esse username."
            })

        # Diferencia entre Personal e Entusiasta
        if tipo == "personal":
            user.is_personal = True
            user.save()
            Personal.objects.create(user=user, registroProfissional=request.POST['registroProfissional'])
        elif tipo == "entusiasta":
            user.is_entusiasta = True
            user.save()
            personal_username = request.POST['personal']
            try:
                personal_user = Usuario.objects.get(username=personal_username, is_personal=True)
                personal = personal_user.personal
            except (Usuario.DoesNotExist, AttributeError):
                return render(request, "netFitApp/register.html", {
                    "msg_erro": "Personal inválido."
                })
            Entusiasta.objects.create(
                user=user,
                percentualDeGordura=request.POST['percentualDeGordura'],
                peso=request.POST['peso'],
                personal=personal
            )

        # Loga o usuário automaticamente após o registro
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "netFitApp/register.html")


# Retorna a página que lista os treinos do usuário
@login_required(login_url='/login')
def listar_treinos(request):
    treinos = Treino.objects.filter(entusiasta=request.user).prefetch_related('series__exercicio')
    return render(request, 'netFitApp/listarTreinos.html', {'treinos':treinos})


# Retorna a página enviar treino e lida com as requisições POST do seu formulário
@login_required(login_url='/login')
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
    return render(request, 'netFitApp/criarTreino.html', {'treino_form':treino_form}, {'series_form':series_form})
