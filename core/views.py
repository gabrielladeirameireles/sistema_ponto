from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import PontoDiario, SolicitacaoAjuste
from .forms import SolicitacaoAjusteForm

# Função auxiliar de permissão
def eh_rh(user):
    return user.is_authenticated and (user.tipo == 'RH' or user.is_superuser)


@login_required
def registrar_ponto(request):
    hoje = timezone.localtime().date()
    agora = timezone.localtime().time()

    ponto, _ = PontoDiario.objects.get_or_create(
        usuario=request.user,
        data=hoje
    )

    if request.method == 'POST' and 'bater_ponto' in request.POST:
        if not ponto.entrada_1:
            ponto.entrada_1 = agora
            mensagem = "Entrada 1 registrada com sucesso!"
        elif not ponto.saida_1:
            ponto.saida_1 = agora
            mensagem = "Saída para o almoço registrada com sucesso!"
        elif not ponto.entrada_2:
            ponto.entrada_2 = agora
            mensagem = "Retorno do almoço registrado com sucesso!"
        elif not ponto.saida_2:
            ponto.saida_2 = agora
            mensagem = "Saída 2 registrada com sucesso!"
        else:
            messages.warning(request, "Todas as marcações de hoje já foram realizadas.")
            return redirect('registrar_ponto')

        ponto.save()
        messages.success(request, mensagem)
        return redirect('registrar_ponto')

    # Formulário de Ajuste
    form_ajuste = SolicitacaoAjusteForm()
    if request.method == 'POST' and 'solicitar_ajuste' in request.POST:
        form_ajuste = SolicitacaoAjusteForm(request.POST)
        if form_ajuste.is_valid():
            solicitacao = form_ajuste.save(commit=False)
            solicitacao.usuario = request.user
            solicitacao.save()
            messages.success(request, "Solicitação de ajuste enviada com sucesso!")
            return redirect('registrar_ponto')

    historico = PontoDiario.objects.filter(usuario=request.user).order_by('-data')[:7]
    minhas_solicitacoes = SolicitacaoAjuste.objects.filter(usuario=request.user).order_by('-criado_em')[:5]

    return render(request, 'registrar_ponto.html', {
        'ponto': ponto,
        'hoje': hoje,
        'historico': historico,
        'form_ajuste': form_ajuste,
        'minhas_solicitacoes': minhas_solicitacoes
    })


# --- VIEWS DO PAINEL RH ---

@login_required
@user_passes_test(eh_rh, login_url='registrar_ponto')
def painel_rh(request):
    solicitacoes_pendentes = SolicitacaoAjuste.objects.filter(status='PENDENTE').order_by('-criado_em')
    historico_solicitacoes = SolicitacaoAjuste.objects.exclude(status='PENDENTE').order_by('-criado_em')[:10]

    return render(request, 'painel_rh.html', {
        'pendentes': solicitacoes_pendentes,
        'historico': historico_solicitacoes
    })


@login_required
@user_passes_test(eh_rh, login_url='registrar_ponto')
def responder_solicitacao(request, solicitacao_id, acao):
    solicitacao = get_object_or_404(SolicitacaoAjuste, id=solicitacao_id)

    if acao == 'aprovar':
        solicitacao.status = 'APROVADO'
        solicitacao.save()

        # Atualiza o registro de ponto do funcionário
        ponto, _ = PontoDiario.objects.get_or_create(
            usuario=solicitacao.usuario,
            data=solicitacao.data_referencia
        )
        setattr(ponto, solicitacao.campo_alterado, solicitacao.novo_horario)
        ponto.save()

        messages.success(request, f"Solicitação de {solicitacao.usuario.username} APROVADA e ponto atualizado.")

    elif acao == 'recusar':
        solicitacao.status = 'RECUSADO'
        solicitacao.save()
        messages.warning(request, f"Solicitação de {solicitacao.usuario.username} RECUSADA.")

    return redirect('painel_rh')