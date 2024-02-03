from django.apps import AppConfig


class proxyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'proxy'


    def ready(self) -> None:
        from .utils import buildJsFiles
        buildJsFiles()