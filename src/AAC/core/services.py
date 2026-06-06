from django.db import models
from .models import AtividadeComplementar

def calcular_horas_validadas(aluno, atividade):
    tipo = atividade.tipo_atividade

    horas_solicitadas = atividade.carga_horaria_solicitada

    limite_por_evento = tipo.limite_horas_por_evento
    limite_total = tipo.limite_horas_total

    horas_ja_validadas = AtividadeComplementar.objects.filter(
        aluno=aluno,
        tipo_atividade=tipo,
        status=AtividadeComplementar.Status.VALIDADO
    ).exclude(
        id=atividade.id
    ).aggregate(
        total=models.Sum('carga_horaria_validada')
    )['total'] or 0

    limite_restante = limite_total - horas_ja_validadas

    horas_validadas = min(
        horas_solicitadas,
        limite_por_evento,
        limite_restante
    )

    if horas_validadas < 0:
        horas_validadas = 0

    return horas_validadas