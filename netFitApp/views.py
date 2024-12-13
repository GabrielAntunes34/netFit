from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import *

def index(request):
    return  render(request, "netFitApp/index.html", {
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
            login(request, user)
            return HttpResponseRedirect(reverse("criarTreino"))
        else:
            return render(request, "netFitApp/login.html", {
                "msg_erro": "Username/senha inválidos"
            })
    else:
        return render(request, "netFitApp/login.html")
    
def register(request):
    pass

