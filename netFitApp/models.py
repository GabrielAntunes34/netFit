from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo Abstrato Usuario
class Usuario(AbstractUser):
    cpf = models.CharField(max_length=20, null=True)
    data_nascimento = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True  # Isso torna essa classe abstrata

    def __str__(self):
        return self.username

# Subclasse Personal
class Personal(Usuario):
    registroProfissional = models.TextField(null=True)

    # Definindo related_name para evitar o conflito com o modelo User
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='personals',  # Nome do relacionamento reverso
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='personals_permissions',  # Nome do relacionamento reverso
        blank=True
    )

    def __str__(self):
        return f"Personal: {self.username}"


# Subclasse Entusiasta
class Entusiasta(Usuario):
    percentualDeGordura = models.FloatField(null=True)
    peso = models.FloatField(null=True)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='alunos', null=True)

    # Definindo related_name para evitar o conflito com o modelo User
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='entusiastas',  # Nome do relacionamento reverso
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='entusiastas_permissions',  # Nome do relacionamento reverso
        blank=True
    )

    def __str__(self):
        return f"Entusiasta: {self.username}"
    

class Exercicio(models.Model):
    id = models.AutoField(primary_key=True) # Id é a primary key gerada automaticamente pelo bnado
    nome = models.CharField(max_length=100)
    explicacao = models.TextField()
    musculos = models.TextField()

    def __str__(self):
        return self.nome
    
class Treino(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    gastoCalorico = models.FloatField()
    entusiasta = models.ForeignKey(Entusiasta, on_delete=models.CASCADE, related_name='treinos')

    def __str__(self):
        return self.nome

# Um exercício possui muitas séries
# Um treino possui muitas séries
class Serie(models.Model):
    id = models.AutoField(primary_key=True)
    n_repeticoes = models.PositiveIntegerField()
    n_series = models.PositiveIntegerField()
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE, related_name='series')
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='series')

    def __str__(self):
        return f"{self.n_series} séries de {self.n_repeticoes}"
    
    


