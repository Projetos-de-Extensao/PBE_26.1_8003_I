from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):

    class Perfil(models.TextChoices):
        ALUNO = 'ALUNO', 'Aluno'
        COORDENADOR = 'COORDENADOR', 'Coordenador'
        ORG = 'ORG', 'Organização Acadêmica'

    perfil = models.CharField(
        max_length=20,
        choices=Perfil.choices

    )

class Aluno(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE
    )

    matricula = models.CharField(max_length=20)

    curso = models.CharField(max_length=100)

    semestre_ingresso = models.IntegerField()

    total_horas_integralizadas = models.IntegerField(default=0)

    def str(self):
        return self.usuario.username

class Coordenador(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE
    )

    sia_funcionario = models.CharField(max_length=20)

    def str(self):
        return self.usuario.username
    
class OrgAcademica(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE
    )

    nome_entidade = models.CharField(max_length=100)

    cargo_representante = models.CharField(max_length=100)

    def str(self):
        return self.nome_entidade
class EixoTematico(models.Model):

    nome = models.CharField(max_length=100)

    def str(self):
        return self.nome
class TipoAtividade(models.Model):

    nome = models.CharField(max_length=100)

    limite_horas_total = models.IntegerField()

    limite_horas_por_evento = models.IntegerField()

    eixo_tematico = models.ForeignKey(
        EixoTematico,
        on_delete=models.CASCADE,
        related_name='tipos_atividade'
    )

    def __str__(self):
        return self.nome
class AtividadeComplementar(models.Model):

    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        VALIDADO = 'VALIDADO', 'Validado'
        REJEITADO = 'REJEITADO', 'Rejeitado'

    class Origem(models.TextChoices):
        INTERNA = 'INTERNA', 'Interna'
        EXTERNA = 'EXTERNA', 'Externa'

    descricao = models.TextField()

    carga_horaria_solicitada = models.IntegerField()

    carga_horaria_validada = models.IntegerField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE
    )

    tipo_origem = models.CharField(
        max_length=20,
        choices=Origem.choices
    )

    caminho_comprovante = models.FileField(
        upload_to='comprovantes/'
    )

    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name='atividades'
    )

    coordenador = models.ForeignKey(
        Coordenador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    organizacao = models.ForeignKey(
        OrgAcademica,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    tipo_atividade = models.ForeignKey(
        TipoAtividade,
        on_delete=models.CASCADE
    )

    def str(self):
        return self.descricao
class Validacao(models.Model):

    atividade = models.OneToOneField(
        AtividadeComplementar,
        on_delete=models.CASCADE
    )

    data_analise = models.DateTimeField(auto_now_add=True)

    justificativa = models.TextField()

    def str(self):
        return f'Validação #{self.id}'                    