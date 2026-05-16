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