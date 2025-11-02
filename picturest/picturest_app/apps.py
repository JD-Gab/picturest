from django.apps import AppConfig


class PicturestAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'picturest_app'

    def ready(self):
        import picturest_app.signals
