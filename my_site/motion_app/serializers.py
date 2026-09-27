from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile, Member_Profile, Team, TeamMember, Project, ProjectMember, ClientRequest

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'user_role': self.user.user_role,
        }
        return data


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'position', 'user_role')


class UserProfileDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'email', 'password', 'phone_number',
            'position', 'bio', 'avatar', 'cv_file', 'user_role', 'is_active',
        )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = UserProfile.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class MemberProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member_Profile
        fields = ('id', 'firstName', 'lastName', 'position', 'members_avatar', 'status')


class MemberProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member_Profile
        fields = (
            'id', 'firstName', 'lastName', 'members_avatar', 'bio', 'position',
            'skills', 'github', 'linkedin', 'portfolio', 'resume', 'status',
        )


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'team_name', 'team_image')


class TeamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'team_name', 'descriptions', 'team_image', 'created_at')


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ('id', 'team', 'user', 'role')
        read_only_fields = ('team',)


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'project_status', 'category', 'preview_image')


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description', 'project_status', 'category',
            'preview_image', 'demo_url', 'github_url', 'created_at',
        )


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