from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .api import (
    UsuarioViewSet,
    AlunoViewSet,
    CoordenadorViewSet,
    OrgAcademicaViewSet,
    EixoTematicoViewSet,
    TipoAtividadeViewSet,
    AtividadeComplementarViewSet,
    ValidacaoViewSet
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

router.register(r'alunos', AlunoViewSet)

router.register(r'coordenadores', CoordenadorViewSet)

router.register(r'organizacoes', OrgAcademicaViewSet)

router.register(r'eixos', EixoTematicoViewSet)

router.register(r'tipos-atividade', TipoAtividadeViewSet)

router.register(r'atividades', AtividadeComplementarViewSet)

router.register(r'validacoes', ValidacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
