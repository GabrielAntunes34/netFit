from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    cpf = models.CharField(max_length=20, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)

    # Adicionando campos para diferenciar os tipos de usuários
    is_personal = models.BooleanField(default=False)
    is_entusiasta = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Personal(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='personal', null=True)
    registroProfissional = models.TextField(null=True)

    def __str__(self):
        return f"Personal: {self.user.username}"


class Entusiasta(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='entusiasta', null=True)
    percentualDeGordura = models.FloatField(null=True)
    peso = models.FloatField(null=True)
    personal = models.ForeignKey(Personal, on_delete=models.SET_NULL, related_name='alunos', null=True)

    def __str__(self):
        return f"Entusiasta: {self.user.username}"    

class Exercicio(models.Model):
    id = models.AutoField(primary_key=True) # Id é a primary key gerada automaticamente pelo bnado
    nome = models.CharField(max_length=100)
    explicacao = models.TextField()
    musculos = models.TextField()

    def __str__(self):
        return self.nome
    
# Um exercício possui muitas séries
# Um treino possui muitas séries
class Serie(models.Model):
    id = models.AutoField(primary_key=True)
    n_repeticoes = models.PositiveIntegerField()
    n_series = models.PositiveIntegerField()
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE, related_name='series')

    def __str__(self):
        return f"{self.n_series} séries de {self.n_repeticoes}"
    
class Treino(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    gastoCalorico = models.FloatField()
    series = models.ManyToManyField(Serie, related_name='treinos')
    entusiasta = models.ForeignKey(Entusiasta, on_delete=models.CASCADE, related_name='treinos')

    def __str__(self):
        return self.nome

    
    


