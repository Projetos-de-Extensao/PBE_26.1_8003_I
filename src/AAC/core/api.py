from rest_framework import viewsets
from .permissions import IsAluno, IsCoordenador, IsOrgAcademica
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q

from .models import (
    Usuario,
    Aluno,
    Coordenador,
    OrgAcademica,
    EixoTematico,
    TipoAtividade,
    AtividadeComplementar,
    Validacao
)

from .serializers import (
    UsuarioSerializer,
    AlunoSerializer,
    CoordenadorSerializer,
    OrgAcademicaSerializer,
    EixoTematicoSerializer,
    TipoAtividadeSerializer,
    AtividadeComplementarSerializer,
    AtividadeComplementarWriteSerializer,
    ValidacaoSerializer,
    ValidacaoWriteSerializer
)

class UsuarioViewSet(viewsets.ModelViewSet):

    queryset = Usuario.objects.all()

    serializer_class = UsuarioSerializer

class AlunoViewSet(viewsets.ModelViewSet):

    queryset = Aluno.objects.all()

    serializer_class = AlunoSerializer

class CoordenadorViewSet(viewsets.ModelViewSet):

    queryset = Coordenador.objects.all()

    serializer_class = CoordenadorSerializer

class OrgAcademicaViewSet(viewsets.ModelViewSet):

    queryset = OrgAcademica.objects.all()

    serializer_class = OrgAcademicaSerializer

class EixoTematicoViewSet(viewsets.ModelViewSet):

    queryset = EixoTematico.objects.all()

    serializer_class = EixoTematicoSerializer

class TipoAtividadeViewSet(viewsets.ModelViewSet):

    queryset = TipoAtividade.objects.all()

    serializer_class = TipoAtividadeSerializer

class AtividadeComplementarViewSet(viewsets.ModelViewSet):

    queryset = AtividadeComplementar.objects.all()

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AtividadeComplementarWriteSerializer
        return AtividadeComplementarSerializer
    
    def get_queryset(self):
        usuario = self.request.user

        if usuario.perfil == 'ALUNO':
            aluno = Aluno.objects.get(usuario=usuario)

            return AtividadeComplementar.objects.filter(
                Q(aluno=aluno) |
                Q(alunos_participantes=aluno)
            ).distinct()

        elif usuario.perfil == 'COORDENADOR':
            coordenador = Coordenador.objects.get(usuario=usuario)

            return AtividadeComplementar.objects.filter(
                Q(coordenador=coordenador) |
                Q(status=AtividadeComplementar.Status.PENDENTE)
            ).distinct()

        elif usuario.perfil == 'ORG':
            org = OrgAcademica.objects.get(usuario=usuario)

            return AtividadeComplementar.objects.filter(
                organizacao=org
            )

        return AtividadeComplementar.objects.none()

    def perform_create(self, serializer):
        usuario = self.request.user

        if usuario.perfil == 'ALUNO':
            aluno = Aluno.objects.get(usuario=usuario)

            serializer.save(
                aluno=aluno,
                tipo_origem=AtividadeComplementar.Origem.EXTERNA,
                status=AtividadeComplementar.Status.PENDENTE,
                carga_horaria_validada=None
            )

        elif usuario.perfil == 'COORDENADOR':
            coordenador = Coordenador.objects.get(usuario=usuario)

            serializer.save(
                coordenador=coordenador,
                tipo_origem=AtividadeComplementar.Origem.INTERNA,
                status=AtividadeComplementar.Status.ABERTA,
                carga_horaria_validada=None
            )

        elif usuario.perfil == 'ORG':
            org = OrgAcademica.objects.get(usuario=usuario)

            serializer.save(
                organizacao=org,
                tipo_origem=AtividadeComplementar.Origem.INTERNA,
                status=AtividadeComplementar.Status.ABERTA,
                carga_horaria_validada=None
            )

class ValidacaoViewSet(viewsets.ModelViewSet):

    queryset = Validacao.objects.all()

    permission_classes = [IsCoordenador]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ValidacaoWriteSerializer
        return ValidacaoSerializer

    def perform_create(self, serializer):
        validacao = serializer.save()

        atividade = validacao.atividade

        atividade.status = AtividadeComplementar.Status.VALIDADO
        atividade.carga_horaria_validada = atividade.carga_horaria_solicitada
        atividade.coordenador = self.request.user.coordenador
        atividade.save()

        horas = atividade.carga_horaria_validada

        if atividade.tipo_origem == AtividadeComplementar.Origem.EXTERNA:
            aluno = atividade.aluno
            aluno.total_horas_integralizadas += horas
            aluno.save()

        elif atividade.tipo_origem == AtividadeComplementar.Origem.INTERNA:
            for aluno in atividade.alunos_participantes.all():
                aluno.total_horas_integralizadas += horas
                aluno.save()