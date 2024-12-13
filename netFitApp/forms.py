from django import forms
from django.forms.models import inlineformset_factory
from .models import Treino, Serie

# Formulário usado para um cliente criar um novo treino
class TreinoForm(forms.ModelForm):
    class Meta:
        model = Treino
        fields = ['nome', 'gastoCalorico']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'gastoCalorico': forms.TextInput(attrs={'class': 'form-control'}),
        }

# inLineFormSet para associar uma lista de séries ao formulário de treino
SerieInlineFormSet = inlineformset_factory(
    Treino,  # Modelo pai
    Serie,  # Modelo filho
    fields=['n_repeticoes', 'n_series', 'exercicio'],
    extra=3,  # Número de formulários vazios exibidos
    can_delete=True  # Permite excluir séries
)
