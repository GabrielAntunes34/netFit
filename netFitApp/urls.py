from django.urls import path 
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout_view"),
    path("criarTreino/", views.montar_treino, name="criarTreino"),
    path("listarTreinos/", views.listar_treinos, name="listarTreinos")
]