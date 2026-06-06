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
        fields = '__all__'

class CoordenadorSerializer(serializers.ModelSerializer):

    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Coordenador
        fields = '__all__'

class OrgAcademicaSerializer(serializers.ModelSerializer):

    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = OrgAcademica
        fields = '__all__'

class EixoTematicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = EixoTematico
        fields = '__all__'

class TipoAtividadeSerializer(serializers.ModelSerializer):

    eixo_tematico = EixoTematicoSerializer(read_only=True)

    class Meta:
        model = TipoAtividade
        fields = '__all__'

class AtividadeComplementarSerializer(serializers.ModelSerializer):

    aluno = AlunoSerializer(read_only=True)

    alunos_participantes = AlunoSerializer(many=True, read_only=True)

    coordenador = CoordenadorSerializer(read_only=True)

    organizacao = OrgAcademicaSerializer(read_only=True)

    tipo_atividade = TipoAtividadeSerializer(read_only=True)

    class Meta:
        model = AtividadeComplementar
        fields = '__all__'

class ValidacaoSerializer(serializers.ModelSerializer):

    atividade = AtividadeComplementarSerializer(read_only=True)

    class Meta:
        model = Validacao
        fields = '__all__'

class AtividadeComplementarWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtividadeComplementar
        fields = [
            'descricao',
            'carga_horaria_solicitada',
            'tipo_atividade',
            'caminho_comprovante',
        ]        

class ValidacaoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Validacao
        fields = [
            'atividade',
            'justificativa'
        ]        