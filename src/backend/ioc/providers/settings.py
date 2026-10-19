from dishka import Provider, Scope, provide

from backend.settings import Settings, load_settings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return load_settings()
