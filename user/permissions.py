from rest_framework import permissions

class IsInGroup(permissions.BasePermission):
    """
    Permiso personalizado que permite el acceso solo a usuarios en grupos específicos.
    """

    def __init__(self, group_names):
        self.group_names = group_names

    def has_permission(self, request, view):
        # Verifica si el usuario está autenticado
        if not request.user.is_authenticated:
            return False
        
        # Verifica si el usuario pertenece a uno de los grupos especificados
        return any(group.name in self.group_names for group in request.user.groups.all())