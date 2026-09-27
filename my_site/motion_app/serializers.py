from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile, MemberProfile, Team, TeamMember, Project, ProjectMember, ClientRequest

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'login': self.user.login,
            'role': self.user.role,
            'status': self.user.status
        }
        return data


class MemberProfileSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()

    class Meta:
        model = MemberProfile
        fields = ("id", "firstName", "lastName", "members_avatar", "bio", "position", "skills", "github", "linkedin", "portfolio", "resume", "status", "projects")

    def get_projects(self, obj):
        projects = Project.objects.filter(members__user=obj.member_users).distinct()
        return ProjectListSerializer(projects, many=True).data

class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'login', 'role', 'status')


class UserProfileDetailSerializer(serializers.ModelSerializer):
    member_profile = MemberProfileSerializer(read_only=True)  # Профиль участника

    class Meta:
        model = UserProfile
        fields = ("id", "login", "password", "role", "status", "created_at", "member_profile")
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = UserProfile.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class MemberProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = ("id", "firstName", "lastName", "position", "members_avatar", "status")


class MemberProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = (
            'id', 'firstName', 'lastName', 'members_avatar', 'bio', 'position',
            'skills', 'github', 'linkedin', 'portfolio', 'resume', 'status',
        )


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'team_name', 'team_image')


class TeamDetailSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = ("id", "team_name", "descriptions", "team_image", "created_at", "members")

    def get_members(self, obj):
        return TeamMemberSerializer(obj.members.all(), many=True).data


class TeamMemberSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    class Meta:
        model = TeamMember
        fields = ("id", "user", "role")
        read_only_fields = ("id",)


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'project_status', 'category', 'preview_image')


class ProjectDetailSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()  # Участники проекта

    class Meta:
        model = Project
        fields = ("id", "name", "description", "project_status", "category", "preview_image", "demo_url", "github_url", "created_at", "members")

    def get_members(self, obj):
        return ProjectMemberSerializer(obj.members.all(), many=True).data



class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ('id', 'project', 'user', 'role')
        read_only_fields = ('project',)



class ClientRequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRequest
        fields = ('id', 'name', 'title', 'status', 'created_at')


class ClientRequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRequest
        fields = (
            'id', 'name', 'company', 'email', 'phone', 'title', 'description',
            'project_type', 'budget', 'status', 'created_at',
        )