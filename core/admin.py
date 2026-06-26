from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'matricula', 'curso', 'semestre_ingresso', 'total_horas_integralizadas')
    list_filter = ('curso', 'semestre_ingresso', 'total_horas_integralizadas')
    search_fields = ('matricula',)

class CoordenadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'sia_funcionario')
    search_fields = ('sia_funcionario',)

class OrgAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nome_entidade')
    search_fields = ('nome_entidade',)          

class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'tipo_origem', 'status')
    list_filter = ('tipo_origem', 'status')
    search_fields = ('descricao',)

class EixoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)    

class TipoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'eixo_tematico', 'limite_horas_total', 'limite_horas_por_evento')
    list_filter = ('nome',)
    search_fields = ('nome',) 

admin.site.register(Usuario, UserAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Coordenador, CoordenadorAdmin)
admin.site.register(EixoTematico, EixoAdmin)
admin.site.register(TipoAtividade, TipoAdmin)
admin.site.register(AtividadeComplementar, AtividadeAdmin)
admin.site.register(Validacao)
admin.site.register(OrgAcademica, OrgAdmin)