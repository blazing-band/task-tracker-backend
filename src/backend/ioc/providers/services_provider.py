from dishka import Provider, Scope, provide

from backend.services import EmailProducer, IdentityProvider, JwtService, PasswordHasher, TransactionManager


class ServicesProvider(Provider):
    password_hasher = provide(PasswordHasher, scope=Scope.REQUEST)
    transaction_manager = provide(TransactionManager, scope=Scope.REQUEST)
    jwt_service = provide(JwtService, scope=Scope.REQUEST)
    identity_provider = provide(IdentityProvider, scope=Scope.REQUEST)
    email_producer = provide(EmailProducer, scope=Scope.APP)
