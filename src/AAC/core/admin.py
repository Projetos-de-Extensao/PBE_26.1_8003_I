from django.contrib import admin
from .models import *

admin.site.register(Usuario)
admin.site.register(Aluno)
admin.site.register(Coordenador)
admin.site.register(EixoTematico)
admin.site.register(TipoAtividade)
admin.site.register(AtividadeComplementar)
admin.site.register(Validacao)
admin.site.register(OrgAcademica)

