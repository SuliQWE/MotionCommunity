from rest_framework import viewsets, generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import PermissionDenied
from .models import UserProfile, Member_Profile, Team, TeamMember, Project, ProjectMember, ClientRequest
from .permission import (
    IsAdmin, IsTeamLead, IsOwnerProfileOrReadOnly,
    IsAdminOrProjectTeamLead, IsAdminOrOwnTeamLead, IsAdminOrOwnProjectTeamLead,
)
from .serializers import (
    UserProfileListSerializer, UserProfileDetailSerializer,
    MemberProfileListSerializer, MemberProfileDetailSerializer,
    TeamListSerializer, TeamDetailSerializer, TeamMemberSerializer,
    ProjectListSerializer, ProjectDetailSerializer, ProjectMemberSerializer,
    ClientRequestListSerializer, ClientRequestDetailSerializer,
    LoginSerializer
)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = [IsAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return UserProfileListSerializer
        return UserProfileDetailSerializer  # содержит логику хэширования пароля



class MemberProfileListAPIView(generics.ListAPIView):
    queryset = Member_Profile.objects.all()
    serializer_class = MemberProfileListSerializer
    permission_classes = [AllowAny]


class MemberProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Member_Profile.objects.all()
    serializer_class = MemberProfileDetailSerializer
    http_method_names = ['get', 'patch']
    permission_classes = [IsOwnerProfileOrReadOnly]


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    permission_classes = [IsAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamListSerializer
        return TeamDetailSerializer



class TeamMemberViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAdminOrOwnTeamLead]
    lookup_field = 'user_id'
    lookup_url_kwarg = 'userId'

    def get_queryset(self):
        return TeamMember.objects.filter(team_id=self.kwargs['teamId'])

    def perform_create(self, serializer):
        if serializer.validated_data.get('role') == 'Team_Lead' and self.request.user.user_role != 'Admin':
            raise PermissionDenied('Назначать Team Lead может только Admin')
        serializer.save(team_id=self.kwargs['teamId'])


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        if self.action == 'create':
            return [IsAdmin()]
        return [IsAdminOrProjectTeamLead()]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectDetailSerializer

class ProjectMemberViewSet(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAdminOrOwnProjectTeamLead]
    lookup_field = 'user_id'
    lookup_url_kwarg = 'userId'

    def get_queryset(self):
        return ProjectMember.objects.filter(project_id=self.kwargs['projectId'])

    def perform_create(self, serializer):
        if serializer.validated_data.get('role') == 'Team_Lead' and self.request.user.user_role != 'Admin':
            raise PermissionDenied('Назначать Team Lead может только Admin')
        serializer.save(project_id=self.kwargs['projectId'])


class ClientRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = ClientRequest.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAdmin()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ClientRequestDetailSerializer
        return ClientRequestListSerializer

class ClientRequestDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = ClientRequest.objects.all()
    serializer_class = ClientRequestDetailSerializer
    permission_classes = [IsAdmin]
    http_method_names = ['get', 'patch']