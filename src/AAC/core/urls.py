from django.urls import path
from . import views

urlpatterns = [
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
        'dashboard/coordenador/',
        views.dashboard_coordenador,
        name='dashboard_coordenador'
    ),

    path(
        'dashboard/organizacao/',
        views.dashboard_org,
        name='dashboard_org'
    ),

    path('logout/', views.logout_view, name='logout'),
]