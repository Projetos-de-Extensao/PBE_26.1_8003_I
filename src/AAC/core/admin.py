from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'matricula', 'curso', 'semestre_ingresso', 'total_horas_integralizadas')
    list_filter = ('curso', 'semestre_ingresso', 'total_horas_integralizadas')
    search_fields = ('matricula',)

admin.site.register(Usuario, UserAdmin)

admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Coordenador)
admin.site.register(EixoTematico)
admin.site.register(TipoAtividade)
admin.site.register(AtividadeComplementar)
admin.site.register(Validacao)
admin.site.register(OrgAcademica)