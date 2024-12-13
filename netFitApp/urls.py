from django.urls import path 
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("/criarTreino/", views.index, name="criarTreino"),
    path("/listarTreinos/", views.index, name="listarTreinos")
]