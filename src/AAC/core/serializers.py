from rest_framework import serializers

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

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'email',
            'perfil'
        ]

class AlunoSerializer(serializers.ModelSerializer):

    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Aluno
        fields = 'all'

class CoordenadorSerializer(serializers.ModelSerializer):

    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Coordenador
        fields = 'all'

class OrgAcademicaSerializer(serializers.ModelSerializer):

    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = OrgAcademica
        fields = 'all'

class EixoTematicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = EixoTematico
        fields = 'all'

class TipoAtividadeSerializer(serializers.ModelSerializer):

    eixo_tematico = EixoTematicoSerializer(read_only=True)

    class Meta:
        model = TipoAtividade
        fields = 'all'

class AtividadeComplementarSerializer(serializers.ModelSerializer):

    aluno = AlunoSerializer(read_only=True)

    coordenador = CoordenadorSerializer(read_only=True)

    organizacao = OrgAcademicaSerializer(read_only=True)

    tipo_atividade = TipoAtividadeSerializer(read_only=True)

    class Meta:
        model = AtividadeComplementar
        fields = 'all'

class ValidacaoSerializer(serializers.ModelSerializer):

    atividade = AtividadeComplementarSerializer(read_only=True)

    class Meta:
        model = Validacao
        fields = 'all'