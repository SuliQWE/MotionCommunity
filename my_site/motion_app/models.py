from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


Status_Choices = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)

RoleChoices = (
    ('Admin', 'Администратор'),
    ('Team_Lead', 'Тим Лид'),
    ('Developer', 'Разработчик'),
)


class UserProfileManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError("Логин обязателен")
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(login, password, **extra_fields)


class UserProfile(AbstractUser):
    username = None
    login = models.CharField("Логин для входа", max_length=150, unique=True)
    role = models.CharField("Роль", max_length=20, choices=RoleChoices, default="Developer")
    status = models.CharField("Статус", max_length=20, choices=Status_Choices, default="Active")
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True, null=True, blank=True)

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []

    objects = UserProfileManager()

    def __str__(self):
        return self.login


class MemberProfile(models.Model):
    member_users = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='member_profile')
    firstName = models.CharField(max_length=150)
    lastName = models.CharField(max_length=150)
    members_avatar = models.ImageField('Аватар Участника', upload_to='members_image/', blank=True, null=True)
    bio = models.TextField(blank=True)

    PositonChoices = (
        ('Frontend_Developer', 'Frontend Developer'),
        ('Backend_Developer', 'Backend Developer'),
        ('Fullstack_Developer', 'Fullstack Developer'),
        ('UI/UX_Designer', 'UI/UX Designer'),
        ('QA_Engineer', 'QA Engineer'),
        ('Mobile_Developer', 'Mobile Developer'),
    )

    position = models.CharField(max_length=150, choices=PositonChoices, default='Backend_Developer')
    skills = models.TextField(blank=True)
    github = models.URLField('Гитхаб', blank=True, null=True)
    linkedin = models.URLField('Линкедин', blank=True, null=True)
    portfolio = models.URLField('Портфолио', blank=True, null=True)
    resume = models.FileField('Резюме', upload_to='resume/', blank=True, null=True)
    status = models.CharField(max_length=150, choices=Status_Choices, default='Inactive')

    def __str__(self):
        return f'{self.firstName} {self.lastName}'


class Team(models.Model):
    team_name = models.CharField('Название команды', max_length=255)
    descriptions = models.TextField(blank=True)
    team_image = models.ImageField('Фото Команды', upload_to='team_image/', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.team_name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='team_memberships')
    role = models.CharField(max_length=150, choices=RoleChoices, default='Developer')

    def __str__(self):
        return f'{self.user} - {self.team}'


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    Project_Status = (
        ('Planned', 'Planned'),
        ('In_progress', 'In progress'),
        ('Completed', 'Completed'),
        ('Paused', 'Paused'),
    )
    project_status = models.CharField(max_length=150, choices=Project_Status, default='Planned')
    category = models.CharField(max_length=150)
    preview_image = models.ImageField('Изображение', upload_to='preview_image/', blank=True, null=True)
    demo_url = models.URLField('Демо', blank=True, null=True)
    github_url = models.URLField('Гитхаб', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='project_memberships')
    Member_Role = (
        ('Team_Lead', 'Team Lead'),
        ('Developer', 'Developer'),
    )
    role = models.CharField(max_length=150, choices=Member_Role, default='Developer')

    def __str__(self):
        return f'{self.user} - {self.project}'


class ClientRequest(models.Model):
    name = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    email = models.EmailField()
    phone = PhoneNumberField()
    title = models.CharField(max_length=150)
    description = models.TextField()
    project_type = models.CharField(max_length=150)
    budget = models.PositiveIntegerField(null=True, blank=True)
    Client_Status = (
        ('New', 'New'),
        ('Reviewing', 'Reviewing'),
    )
    status = models.CharField(max_length=150, choices=Client_Status, default='New')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.title}'


