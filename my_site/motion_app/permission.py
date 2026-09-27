from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import TeamMember, ProjectMember

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Admin'


class IsTeamLead(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Team_Lead'


class IsOwnerProfileOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.member_users_id == request.user.id


class IsAdminOrProjectTeamLead(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in ('Admin', 'Team_Lead'))

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'Admin':
            return True
        return obj.members.filter(user=request.user, role='Team_Lead').exists()


class IsAdminOrOwnTeamLead(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.role == 'Admin':
            return True
        if user.role != 'Team_Lead':
            return False
        return TeamMember.objects.filter(
            team_id=view.kwargs.get('teamId'), user=user, role='Team_Lead'
        ).exists()


class IsAdminOrOwnProjectTeamLead(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.role == 'Admin':
            return True
        if user.role != 'Team_Lead':
            return False
        return ProjectMember.objects.filter(
            project_id=view.kwargs.get('projectId'), user=user, role='Team_Lead'
        ).exists()
