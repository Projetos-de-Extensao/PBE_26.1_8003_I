from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),

    path(
        'dashboard/aluno/',
        views.dashboard_aluno,
        name='dashboard_aluno'
    ),

    path(
        'atividades/externa/cadastrar/',
        views.cadastrar_atividade_externa,
        name='cadastrar_atividade_externa'
    ),

    path(
        'atividades/internas/<int:atividade_id>/participar/',
        views.participar_atividade_interna,
        name='participar_atividade_interna'
    ),

    path(
        'dashboard/coordenador/',
        views.dashboard_coordenador,
        name='dashboard_coordenador'
    ),

    path(
        'atividades/interna/coordenador/cadastrar/',
        views.cadastrar_atividade_interna_coordenador,
        name='cadastrar_atividade_interna_coordenador'
    ),

    path(
        'atividades/<int:atividade_id>/aprovar/',
        views.aprovar_atividade,
        name='aprovar_atividade'
    ),

    path(
        'atividades/<int:atividade_id>/rejeitar/',
        views.rejeitar_atividade,
        name='rejeitar_atividade'
    ),

    path(
        'dashboard/organizacao/',
        views.dashboard_org,
        name='dashboard_org'
    ),

    path(
        'atividades/interna/organizacao/cadastrar/',
        views.cadastrar_atividade_interna_org,
        name='cadastrar_atividade_interna_org'
    ),

    path(
        'atividades/internas/<int:atividade_id>/',
        views.detalhes_atividade_interna,
        name='detalhes_atividade_interna'
    ),

    path(
        'atividades/<int:atividade_id>/checkin/',
        views.checkin_atividade,
        name='checkin_atividade'
    ),

    path(
        'atividades/<int:atividade_id>/qrcode/',
        views.qrcode_atividade,
        name='qrcode_atividade'
    ),

    path('logout/', views.logout_view, name='logout'),
]