from dishka import Provider, Scope, provide

from backend.settings import load_settings, Settings


class SettingsProvider(Provider):

    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return load_settings()
