from dishka import Provider, Scope, provide

from backend.services import EmailService


class CeleryServicesProvider(Provider):
    email_service = provide(EmailService, scope=Scope.REQUEST)
