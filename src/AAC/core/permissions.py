from rest_framework.permissions import BasePermission


class IsAluno(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.perfil == 'ALUNO'
        )


class IsCoordenador(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.perfil == 'COORDENADOR'
        )


class IsOrgAcademica(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.perfil == 'ORG'
        )