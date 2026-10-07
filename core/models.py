from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# 1. Usuário Personalizado (Funcionário e Gestor/RH)
class Usuario(AbstractUser):
    TIPO_CHOICES = (
        ('FUNCIONARIO', 'Funcionário'),
        ('RH', 'Gestor / RH'),
    )
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='FUNCIONARIO')
    cargo = models.CharField(max_length=100, blank=True, null=True)
    jornada_semanal = models.IntegerField(default=40, help_text="Carga horária semanal em horas (ex: 40 ou 44)")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})" if self.first_name else self.username


# 2. Registro diário de Ponto (4 batidas por dia)
class PontoDiario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pontos')
    data = models.DateField(default=timezone.now)
    
    entrada_1 = models.TimeField(null=True, blank=True, verbose_name="Entrada 1")
    saida_1 = models.TimeField(null=True, blank=True, verbose_name="Saída Almoço")
    entrada_2 = models.TimeField(null=True, blank=True, verbose_name="Retorno Almoço")
    saida_2 = models.TimeField(null=True, blank=True, verbose_name="Saída 2")

    class Meta:
        unique_together = ('usuario', 'data')
        verbose_name = "Ponto Diário"
        verbose_name_plural = "Pontos Diários"

    def __str__(self):
        return f"{self.usuario.username} - {self.data}"


# 3. Solicitação de Ajuste pelo Funcionário (Pendente de Aprovação)
class SolicitacaoAjuste(models.Model):
    STATUS_CHOICES = (
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('RECUSADO', 'Recusado'),
    )
    CAMPO_CHOICES = (
        ('entrada_1', 'Entrada 1'),
        ('saida_1', 'Saída Almoço'),
        ('entrada_2', 'Retorno Almoço'),
        ('saida_2', 'Saída 2'),
    )

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='solicitacoes')
    ponto = models.ForeignKey(PontoDiario, on_delete=models.CASCADE, related_name='ajustes', null=True, blank=True)
    data_referencia = models.DateField(verbose_name="Data do Ponto")
    campo_alterado = models.CharField(max_length=20, choices=CAMPO_CHOICES)
    novo_horario = models.TimeField(verbose_name="Novo Horário")
    justificativa = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDENTE')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ajuste {self.usuario.username} - {self.data_referencia} ({self.status})"