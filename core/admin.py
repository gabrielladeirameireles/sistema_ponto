from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, PontoDiario, SolicitacaoAjuste

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informações de Ponto/RH', {'fields': ('cpf', 'tipo', 'cargo', 'jornada_semanal')}),
    )
    list_display = ('username', 'first_name', 'last_name', 'cpf', 'tipo', 'cargo')

@admin.register(PontoDiario)
class PontoDiarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data', 'entrada_1', 'saida_1', 'entrada_2', 'saida_2')
    list_filter = ('data', 'usuario')

@admin.register(SolicitacaoAjuste)
class SolicitacaoAjusteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_referencia', 'campo_alterado', 'novo_horario', 'status')
    list_filter = ('status', 'data_referencia')