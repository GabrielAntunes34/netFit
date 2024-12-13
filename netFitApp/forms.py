from django import forms
from django.forms.models import inlineformset_factory
from .models import Treino, Serie

# Formulário usado para um cliente criar um novo treino
class formTreino(forms.modelForm):
    class Meta:
        model = Treino
        fields = ['Nome', 'Gasto calórico']

        widgets = {
            'Nome': forms.TextInput(attrs={'class': 'form-control'}),
            'Gasto calórico': forms.TextInput(attrs={'class': 'form-control'}),
        }

# inLineFormSet para associar uma lista de séries ao formulário de treino
SerieInlineFormSet = inlineformset_factory(
    Treino,  # Modelo pai
    Serie,  # Modelo filho
    extra=3,  # Número de formulários vazios exibidos
    can_delete=True  # Permite excluir séries
)
