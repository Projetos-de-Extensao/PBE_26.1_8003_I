from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import qrcode
import base64
from io import BytesIO

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

    atividades_internas = AtividadeComplementar.objects.filter(
        coordenador=coordenador,
        tipo_origem=AtividadeComplementar.Origem.INTERNA
    ).order_by('-id')

    atividades_pendentes = ( AtividadeComplementar.objects.filter(
        status=AtividadeComplementar.Status.PENDENTE
    )
    .select_related('aluno')
    )

    curso = request.GET.get("curso")
    semestre = request.GET.get("semestre")

    if curso:
        atividades_pendentes = atividades_pendentes.filter(
            aluno__curso=curso
        )

    if semestre:
        atividades_pendentes = atividades_pendentes.filter(
            aluno__semestre_ingresso=semestre
        )

    cursos = (
        Aluno.objects
        .values_list("curso", flat=True)
        .distinct()
    )

    semestres = (
        Aluno.objects
        .values_list("semestre_ingresso", flat=True)
        .distinct()
        .order_by('semestre_ingresso')
    )

    return render(
        request,
        "dashboard_coordenador.html",
        {
            "coordenador": coordenador,
            "atividades_pendentes": atividades_pendentes,
            "atividades_internas": atividades_internas,
            "cursos": cursos,
            "semestres": semestres,
            "curso_selecionado": curso,
            "semestre_selecionado": semestre,
        }
    )


@login_required
def dashboard_org(request):
    org = OrgAcademica.objects.get(usuario=request.user)

    atividades_internas = AtividadeComplementar.objects.filter(
        organizacao=org,
        tipo_origem=AtividadeComplementar.Origem.INTERNA
    ).order_by('-id')

    return render(
        request,
        'dashboard_org.html',
        {
            'org': org,
            'atividades_internas': atividades_internas,
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
        palestrante = request.POST.get('palestrante')
        local = request.POST.get('local')
        data_hora_evento = request.POST.get('data_hora_evento')

        tipo_atividade = TipoAtividade.objects.get(id=tipo_atividade_id)

        AtividadeComplementar.objects.create(
            descricao=descricao,
            carga_horaria_solicitada=carga_horaria,
            palestrante=palestrante,
            local=local,
            data_hora_evento=data_hora_evento,
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
        palestrante = request.POST.get('palestrante')
        local = request.POST.get('local')
        data_hora_evento = request.POST.get('data_hora_evento')

        tipo_atividade = TipoAtividade.objects.get(id=tipo_atividade_id)

        AtividadeComplementar.objects.create(
            descricao=descricao,
            carga_horaria_solicitada=carga_horaria,
            palestrante=palestrante,
            local=local,
            data_hora_evento=data_hora_evento,
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

@login_required
def detalhes_atividade_interna(request, atividade_id):

    atividade = AtividadeComplementar.objects.get(
        id=atividade_id,
        tipo_origem=AtividadeComplementar.Origem.INTERNA
    )

    return render(
        request,
        'detalhes_atividade_interna.html',
        {
            'atividade': atividade
        }
    )

@login_required
def checkin_atividade(request, atividade_id):

    aluno = Aluno.objects.get(usuario=request.user)

    atividade = AtividadeComplementar.objects.get(
        id=atividade_id,
        tipo_origem=AtividadeComplementar.Origem.INTERNA,
        status=AtividadeComplementar.Status.ABERTA
    )

    if not atividade.alunos_participantes.filter(id=aluno.id).exists():

        atividade.alunos_participantes.add(aluno)

        aluno.total_horas_integralizadas += (
            atividade.carga_horaria_solicitada
        )

        aluno.save()

    return redirect('dashboard_aluno')

@login_required
def qrcode_atividade(request, atividade_id):

    atividade = AtividadeComplementar.objects.get(
        id=atividade_id
    )

    url_checkin = request.build_absolute_uri(
        f'/atividades/{atividade.id}/checkin/'
    )

    qr = qrcode.make(url_checkin)

    buffer = BytesIO()
    qr.save(buffer, format='PNG')

    qr_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode()

    return render(
        request,
        'qrcode_atividade.html',
        {
            'atividade': atividade,
            'qr_code': qr_base64,
            'url_checkin': url_checkin,
            'perfil': request.user.perfil
        }
    )