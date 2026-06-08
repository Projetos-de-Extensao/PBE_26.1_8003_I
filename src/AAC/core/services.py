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

def aprovar_atividade_service(atividade, coordenador):
    if atividade.status == AtividadeComplementar.Status.VALIDADO:
        return atividade

    if atividade.status not in [
        AtividadeComplementar.Status.PENDENTE,
        AtividadeComplementar.Status.ABERTA
    ]:
        return atividade

    atividade.status = AtividadeComplementar.Status.VALIDADO
    atividade.coordenador = coordenador

    if atividade.tipo_origem == AtividadeComplementar.Origem.EXTERNA:
        aluno = atividade.aluno

        horas_validadas = calcular_horas_validadas(
            aluno,
            atividade
        )

        atividade.carga_horaria_validada = horas_validadas
        atividade.save()

        aluno.total_horas_integralizadas += horas_validadas
        aluno.save()

    elif atividade.tipo_origem == AtividadeComplementar.Origem.INTERNA:
        atividade.carga_horaria_validada = atividade.carga_horaria_solicitada
        atividade.save()

        for aluno in atividade.alunos_participantes.all():
            horas_validadas = calcular_horas_validadas(
                aluno,
                atividade
            )

            aluno.total_horas_integralizadas += horas_validadas
            aluno.save()

    return atividade