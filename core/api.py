from rest_framework import viewsets
from .permissions import IsAluno, IsCoordenador, IsOrgAcademica
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from .services import aprovar_atividade_service

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

    queryset = AtividadeComplementar.objects.select_related(
        'aluno',
        'coordenador',
        'organizacao',
        'tipo_atividade'
    ).prefetch_related(
        'alunos_participantes'
    )

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AtividadeComplementarWriteSerializer
        return AtividadeComplementarSerializer
    
    def get_queryset(self):
        base_queryset = AtividadeComplementar.objects.select_related(
            'aluno',
            'coordenador',
            'organizacao',
            'tipo_atividade'
        ).prefetch_related(
            'alunos_participantes'
        )

        usuario = self.request.user

        if usuario.perfil == 'ALUNO':
            aluno = Aluno.objects.get(usuario=usuario)

            return base_queryset.filter(
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
            
    @action(detail=True, methods=['post'])
    def rejeitar(self, request, pk=None):
        usuario = request.user

        if usuario.perfil != 'COORDENADOR':
            raise PermissionDenied(
                'Apenas coordenadores podem rejeitar atividades.'
            )

        coordenador = Coordenador.objects.get(usuario=usuario)

        atividade = self.get_object()

        if atividade.status != AtividadeComplementar.Status.PENDENTE:
            return Response(
                {
                    'erro': 'Apenas atividades pendentes podem ser rejeitadas.'
                },
                status=400
            )

        atividade.status = AtividadeComplementar.Status.REJEITADO
        atividade.coordenador = coordenador
        atividade.save()

        return Response(
            {
                'mensagem': 'Atividade rejeitada com sucesso.',
                'id': atividade.id,
                'status': atividade.status
            }
        )        

class ValidacaoViewSet(viewsets.ModelViewSet):

    queryset = Validacao.objects.select_related(
        'atividade'
    )

    permission_classes = [IsCoordenador]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ValidacaoWriteSerializer
        return ValidacaoSerializer

    def perform_create(self, serializer):
        validacao = serializer.save()

        atividade = validacao.atividade
        coordenador = self.request.user.coordenador

        aprovar_atividade_service(
            atividade=atividade,
            coordenador=coordenador
        )