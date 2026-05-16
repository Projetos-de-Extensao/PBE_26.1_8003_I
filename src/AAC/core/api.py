from rest_framework import viewsets

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
    ValidacaoSerializer
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

    serializer_class = AtividadeComplementarSerializer
class ValidacaoViewSet(viewsets.ModelViewSet):

    queryset = Validacao.objects.all()

    serializer_class = ValidacaoSerializer