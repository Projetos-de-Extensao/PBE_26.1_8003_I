from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Aluno, Coordenador, OrgAcademica, AtividadeComplementar, TipoAtividade


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
        aluno=aluno
    )

    return render(
        request,
        'dashboard_aluno.html',
        {
            'aluno': aluno,
            'atividades': atividades
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