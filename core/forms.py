from django import forms
from .models import SolicitacaoAjuste

class SolicitacaoAjusteForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoAjuste
        fields = ['data_referencia', 'campo_alterado', 'novo_horario', 'justificativa']
        widgets = {
            'data_referencia': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'campo_alterado': forms.Select(attrs={'class': 'form-control'}),
            'novo_horario': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'justificativa': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Descreva o motivo do ajuste...'}),
        }