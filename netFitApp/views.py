from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TreinoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import *

# Retorna a página inicial do site
def index(request):
    return render(request, "netFitApp/index.html", {
        "user": request.user
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

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
            Personal.objects.create(user=user, registroProfissional=request.POST['registroProfissional'])
            user.save()
        elif tipo == "entusiasta":
            user.is_entusiasta = True
            personal_username = request.POST['personal']
            try:
                personal_user = Usuario.objects.get(username=personal_username, is_personal=True)
            except (Usuario.DoesNotExist, AttributeError):
                return render(request, "netFitApp/register.html", {
                    "msg_erro": "Personal inválido."
                })
            user.save()
            Entusiasta.objects.create(
                user=user,
                percentualDeGordura=request.POST['percentualDeGordura'],
                peso=request.POST['peso'],
                personal=Personal.objects.get(user=personal_user)
            )

        # Loga o usuário automaticamente após o registro
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "netFitApp/register.html")


# Retorna a página que lista os treinos do usuário
@login_required(login_url='/login')
def listar_treinos(request):
    if request.user.is_personal:
        return HttpResponseRedirect(reverse("index"))

    treinos = Treino.objects.filter(entusiasta=Entusiasta.objects.get(user=request.user)).prefetch_related('series__exercicio')
    return render(request, 'netFitApp/listarTreinos.html', {'treinos':treinos})


# Retorna a página enviar treino e lida com as requisições POST do seu formulário
@login_required(login_url='/login')
def montar_treino(request):
    if request.method == "POST":
        # Obtendo os dados de cada formulário da requisição
        treino_form = TreinoForm(request.POST)

        # Se a resposta é valida, Instanciamos o objeto
        if treino_form.is_valid():
            # Salvando o novo objeto de Treino no banco
            treino = treino_form.save(commit=False)

            treino.entusiasta = None
            if (request.user.is_personal):
                alunos = Entusiasta.objects.filter(personal=Personal.objects.get(user=request.user))
                for aluno in alunos:
                    if (aluno.user.username == request.POST['aluno']):
                        treino.entusiasta = aluno
            else:
                treino.entusiasta = Entusiasta.objects.get(user=request.user)

            # Salvando as séries selecionadas na requisição
            series = []

            exercicios_nomes = [ex for ex in Exercicio.objects.filter()]
            for ex in exercicios_nomes:
                if (request.POST[f'{ex.nome}_valido'] == "0"):
                    continue
                    
                num_series = request.POST[f'{ex.nome}_serie']
                num_reps = request.POST[f'{ex.nome}_repeticao']

                serie = Serie(n_series=num_series, n_repeticoes=num_reps, exercicio=ex)
                serie.save()
                series.append(serie)
                
            treino.save()
            treino.series.add(*series)
            treino.save()
            return HttpResponseRedirect(reverse("listarTreinos"))
        
    else:
        # Se não, a requisição é um get, e apenas respondemos com a página com os formulários
        treino_form = TreinoForm()

        alunos = None
        if request.user.is_personal:
            personal = Personal.objects.get(user=request.user)
            try:
                alunos = [a.user for a in Entusiasta.objects.filter(personal=personal)]
            except:
                pass

        exercicios = Exercicio.objects.filter()
        return render(request, 'netFitApp/criarTreino.html', {'treino_form':treino_form, 'alunos': alunos, 'exercicios': exercicios})
