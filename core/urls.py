from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.registrar_ponto, name='registrar_ponto'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('rh/', views.painel_rh, name='painel_rh'),
    path('rh/solicitacao/<int:solicitacao_id>/<str:acao>/', views.responder_solicitacao, name='responder_solicitacao'),
]