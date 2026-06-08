from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Aluno, Coordenador, OrgAcademica, AtividadeComplementar, TipoAtividade
from .services import (
    calcular_horas_validadas,
    aprovar_atividade_service
)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            login(request, usuario)

            if usuario.perfil == 'ALUNO':
                return redirect('dashboard_aluno')

            if usuario.perfil == 'COORDENADOR':
                return redirect('dashboard_coordenador')

            if usuario.perfil == 'ORG':
                return redirect('dashboard_org')

        return render(
            request,
            'login.html',
            {'erro': 'Usuário ou senha inválidos'}
        )

    return render(request, 'login.html')


@login_required
def dashboard_aluno(request):
    aluno = Aluno.objects.get(usuario=request.user)

    atividades = AtividadeComplementar.objects.filter(
        Q(aluno=aluno) | Q(alunos_participantes=aluno)
    ).distinct()

    atividades_internas_abertas = AtividadeComplementar.objects.filter(
        tipo_origem=AtividadeComplementar.Origem.INTERNA,
        status=AtividadeComplementar.Status.ABERTA
    ).exclude(
        alunos_participantes=aluno
    )

    HORAS_NECESSARIAS = 140

    return render(
        request,
        'dashboard_aluno.html',
        {
            'aluno': aluno,
            'atividades': atividades,
            'atividades_internas_abertas': atividades_internas_abertas,
            'horas_necessarias': HORAS_NECESSARIAS
        }
    )


@login_required
def dashboard_coordenador(request):
    coordenador = Coordenador.objects.get(usuario=request.user)

    atividades_pendentes = AtividadeComplementar.objects.filter(
        status=AtividadeComplementar.Status.PENDENTE
    )

    return render(
        request,
        'dashboard_coordenador.html',
        {
            'coordenador': coordenador,
            'atividades_pendentes': atividades_pendentes
        }
    )


@login_required
def dashboard_org(request):
    org = OrgAcademica.objects.get(usuario=request.user)

    return render(
        request,
        'dashboard_org.html',
        {
            'org': org
        }
    )


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def cadastrar_atividade_externa(request):
    aluno = Aluno.objects.get(usuario=request.user)
    tipos_atividade = TipoAtividade.objects.all()

    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        carga_horaria = request.POST.get('carga_horaria_solicitada')
        tipo_atividade_id = request.POST.get('tipo_atividade')
        comprovante = request.FILES.get('caminho_comprovante')

        tipo_atividade = TipoAtividade.objects.get(id=tipo_atividade_id)

        AtividadeComplementar.objects.create(
            descricao=descricao,
            carga_horaria_solicitada=carga_horaria,
            tipo_origem=AtividadeComplementar.Origem.EXTERNA,
            status=AtividadeComplementar.Status.PENDENTE,
            aluno=aluno,
            tipo_atividade=tipo_atividade,
            caminho_comprovante=comprovante
        )

        return redirect('dashboard_aluno')

    return render(
        request,
        'cadastrar_atividade_externa.html',
        {
            'aluno': aluno,
            'tipos_atividade': tipos_atividade
        }
    )

@login_required
def participar_atividade_interna(request, atividade_id):
    aluno = Aluno.objects.get(usuario=request.user)

    atividade = AtividadeComplementar.objects.get(
        id=atividade_id,
        tipo_origem=AtividadeComplementar.Origem.INTERNA,
        status=AtividadeComplementar.Status.ABERTA
    )

    if not atividade.alunos_participantes.filter(id=aluno.id).exists():
        atividade.alunos_participantes.add(aluno)

        aluno.total_horas_integralizadas += atividade.carga_horaria_solicitada
        aluno.save()

    return redirect('dashboard_aluno')

@login_required
def cadastrar_atividade_interna_coordenador(request):
    coordenador = Coordenador.objects.get(usuario=request.user)
    tipos_atividade = TipoAtividade.objects.all()

    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        carga_horaria = request.POST.get('carga_horaria_solicitada')
        tipo_atividade_id = request.POST.get('tipo_atividade')

        tipo_atividade = TipoAtividade.objects.get(id=tipo_atividade_id)

        AtividadeComplementar.objects.create(
            descricao=descricao,
            carga_horaria_solicitada=carga_horaria,
            tipo_origem=AtividadeComplementar.Origem.INTERNA,
            status=AtividadeComplementar.Status.ABERTA,
            coordenador=coordenador,
            tipo_atividade=tipo_atividade
        )

        return redirect('dashboard_coordenador')

    return render(
        request,
        'cadastrar_atividade_interna.html',
        {
            'tipos_atividade': tipos_atividade,
            'tipo_usuario': 'Coordenador',
            'voltar_url': 'dashboard_coordenador'
        }
    )

@login_required
def cadastrar_atividade_interna_org(request):
    org = OrgAcademica.objects.get(usuario=request.user)
    tipos_atividade = TipoAtividade.objects.all()

    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        carga_horaria = request.POST.get('carga_horaria_solicitada')
        tipo_atividade_id = request.POST.get('tipo_atividade')

        tipo_atividade = TipoAtividade.objects.get(id=tipo_atividade_id)

        AtividadeComplementar.objects.create(
            descricao=descricao,
            carga_horaria_solicitada=carga_horaria,
            tipo_origem=AtividadeComplementar.Origem.INTERNA,
            status=AtividadeComplementar.Status.ABERTA,
            organizacao=org,
            tipo_atividade=tipo_atividade
        )

        return redirect('dashboard_org')

    return render(
        request,
        'cadastrar_atividade_interna.html',
        {
            'tipos_atividade': tipos_atividade,
            'tipo_usuario': 'Organização Acadêmica',
            'voltar_url': 'dashboard_org'
        }
    )

@login_required
def aprovar_atividade(request, atividade_id):
    coordenador = Coordenador.objects.get(usuario=request.user)

    atividade = AtividadeComplementar.objects.get(
        id=atividade_id,
        status=AtividadeComplementar.Status.PENDENTE
    )

    aprovar_atividade_service(
        atividade=atividade,
        coordenador=coordenador
    )

    return redirect('dashboard_coordenador')


@login_required
def rejeitar_atividade(request, atividade_id):
    coordenador = Coordenador.objects.get(usuario=request.user)

    atividade = AtividadeComplementar.objects.get(
        id=atividade_id,
        status=AtividadeComplementar.Status.PENDENTE
    )

    atividade.status = AtividadeComplementar.Status.REJEITADO
    atividade.coordenador = coordenador
    atividade.save()

    return redirect('dashboard_coordenador')