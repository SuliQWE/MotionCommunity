"""
Заполняет базу тестовыми данными: 1 Admin, 2 Team Lead, 12 Developer,
5 команд, 5 проектов. Переводимые поля (bio, descriptions, description)
заполняются сразу на русском и английском через modeltranslation.

Использование:
    python manage.py seed_data
Повторный запуск безопасен — всё делается через get_or_create.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from motion_app.models import (
    UserProfile, Member_Profile, Team, TeamMember, Project, ProjectMember,
)


class Command(BaseCommand):
    help = 'Заполняет БД тестовыми пользователями, командами и проектами (RU/EN)'

    @transaction.atomic
    def handle(self, *args, **options):
        admin = self.create_admin()
        leads = self.create_team_leads()
        developers = self.create_developers()
        teams = self.create_teams()
        projects = self.create_projects()

        self.distribute(leads, developers, teams, projects)

        self.stdout.write(self.style.SUCCESS(
            f'Готово: 1 admin, {len(leads)} team lead, {len(developers)} developer, '
            f'{len(teams)} команд, {len(projects)} проектов.'
        ))

    # ---------- Users ----------

    def create_admin(self):
        user, created = UserProfile.objects.get_or_create(
            email='admin@motion.community',
            defaults=dict(
                username='admin',
                position='Platform Administrator',
                user_role='Admin',
                is_staff=True,
                is_superuser=True,
            ),
        )
        if created:
            user.set_password('Admin12345!')
            user.save()
        return user

    def create_team_leads(self):
        data = [
            ('lead1@motion.community', 'nurlan.lead', 'Нурлан', 'Асанов', 'Fullstack_Developer'),
            ('lead2@motion.community', 'aigerim.lead', 'Айгерим', 'Токтогулова', 'Backend_Developer'),
        ]
        leads = []
        for email, username, first, last, position in data:
            user, created = UserProfile.objects.get_or_create(
                email=email,
                defaults=dict(username=username, position='Team Lead', user_role='Team_Lead'),
            )
            if created:
                user.set_password('TeamLead12345!')
                user.save()

            profile, _ = Member_Profile.objects.get_or_create(
                member_users=user,
                defaults=dict(firstName=first, lastName=last, position=position, status='Active'),
            )
            self.set_bio(profile,
                ru=f'{first} {last} — тимлид в Motion Community, ведёт несколько проектов одновременно.',
                en=f'{first} {last} is a team lead at Motion Community, running several projects at once.')
            leads.append(user)
        return leads

    def create_developers(self):
        data = [
            ('dev1@motion.community', 'dev1', 'Азамат', 'Кубанычбеков', 'Frontend_Developer'),
            ('dev2@motion.community', 'dev2', 'Диана', 'Осмонова', 'Frontend_Developer'),
            ('dev3@motion.community', 'dev3', 'Тимур', 'Жумабеков', 'Backend_Developer'),
            ('dev4@motion.community', 'dev4', 'Камила', 'Сыдыкова', 'Backend_Developer'),
            ('dev5@motion.community', 'dev5', 'Эрлан', 'Абдразаков', 'Fullstack_Developer'),
            ('dev6@motion.community', 'dev6', 'Жаннат', 'Мамытова', 'Fullstack_Developer'),
            ('dev7@motion.community', 'dev7', 'Бекзат', 'Орозалиев', 'UI/UX_Designer'),
            ('dev8@motion.community', 'dev8', 'Мээрим', 'Курманбекова', 'UI/UX_Designer'),
            ('dev9@motion.community', 'dev9', 'Данияр', 'Сатыбалдиев', 'QA_Engineer'),
            ('dev10@motion.community', 'dev10', 'Нургуль', 'Бекова', 'QA_Engineer'),
            ('dev11@motion.community', 'dev11', 'Руслан', 'Табылдиев', 'Mobile_Developer'),
            ('dev12@motion.community', 'dev12', 'Салтанат', 'Ибраимова', 'Mobile_Developer'),
        ]
        developers = []
        for email, username, first, last, position in data:
            user, created = UserProfile.objects.get_or_create(
                email=email,
                defaults=dict(username=username, position=position.replace('_', ' '), user_role='Developer'),
            )
            if created:
                user.set_password('Developer12345!')
                user.save()

            profile, _ = Member_Profile.objects.get_or_create(
                member_users=user,
                defaults=dict(firstName=first, lastName=last, position=position, status='Active'),
            )
            self.set_bio(profile,
                ru=f'{first} {last} — участник Motion Community, специализация: {profile.get_position_display()}.',
                en=f'{first} {last} is a Motion Community member specializing in {position.replace("_", " ")}.')
            developers.append(user)
        return developers

    # ---------- Teams ----------

    def create_teams(self):
        data = [
            ('Alpha Team', 'Команда, работающая над образовательными продуктами.',
                           'Team building educational products.'),
            ('Beta Team', 'Команда, отвечающая за клиентские веб-приложения.',
                          'Team responsible for client-facing web applications.'),
            ('Gamma Team', 'Команда мобильной разработки.',
                           'Mobile development team.'),
            ('Delta Team', 'Команда аналитики и внутренних инструментов.',
                           'Analytics and internal tools team.'),
            ('Omega Team', 'Команда, работающая над маркетплейс-проектами.',
                           'Team working on marketplace projects.'),
        ]
        teams = []
        for name, ru, en in data:
            team, _ = Team.objects.get_or_create(team_name=name)
            team.descriptions_ru = ru
            team.descriptions_en = en
            team.save()
            teams.append(team)
        return teams

    # ---------- Projects ----------

    def create_projects(self):
        data = [
            ('Motion LMS Platform', 'Planned', 'Education',
                'Платформа для онлайн-обучения студентов Motion с курсами и тестами.',
                'Online learning platform for Motion students with courses and quizzes.'),
            ('Motion Community Portal', 'In_progress', 'Web',
                'Портал сообщества с профилями участников и проектами.',
                'Community portal with member profiles and project showcase.'),
            ('Motion Mobile Companion', 'In_progress', 'Mobile',
                'Мобильное приложение-компаньон для участников Motion.',
                'Mobile companion app for Motion members.'),
            ('Motion Analytics Dashboard', 'Completed', 'Analytics',
                'Дашборд аналитики успеваемости и активности студентов.',
                'Analytics dashboard for student progress and activity.'),
            ('Motion Marketplace', 'Paused', 'E-commerce',
                'Маркетплейс для продажи цифровых продуктов выпускников.',
                'Marketplace for selling graduates’ digital products.'),
        ]
        projects = []
        for name, status, category, ru, en in data:
            project, _ = Project.objects.get_or_create(
                name=name,
                defaults=dict(project_status=status, category=category, description=ru),
            )
            project.description_ru = ru
            project.description_en = en
            project.save()
            projects.append(project)
        return projects

    # ---------- Распределение по командам/проектам ----------

    def distribute(self, leads, developers, teams, projects):
        # каждому проекту/команде — свой лид (по кругу из 2 лидов) и по 2-3 разработчика
        chunks = [developers[i::5] for i in range(5)]  # делим 12 разработчиков на 5 групп

        for i, (team, project) in enumerate(zip(teams, projects)):
            lead = leads[i % len(leads)]
            group = chunks[i]

            TeamMember.objects.get_or_create(team=team, user=lead, defaults=dict(role='Team_Lead'))
            ProjectMember.objects.get_or_create(project=project, user=lead, defaults=dict(role='Team_Lead'))

            for dev in group:
                TeamMember.objects.get_or_create(team=team, user=dev, defaults=dict(role='Developer'))
                ProjectMember.objects.get_or_create(project=project, user=dev, defaults=dict(role='Developer'))

    # ---------- helpers ----------

    @staticmethod
    def set_bio(profile, ru, en):
        profile.bio_ru = ru
        profile.bio_en = en
        profile.save()