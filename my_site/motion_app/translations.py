
from modeltranslation.translator import TranslationOptions, register
from .models import  Member_Profile, Team, Project, ClientRequest


@register(Member_Profile)
class MemberProfileTranslationOptions(TranslationOptions):
    fields = ( 'bio',)


@register(Team)
class TeamTranslationOptions(TranslationOptions):
    fields = ('descriptions',)


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(ClientRequest)
class ClientRequestTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)
