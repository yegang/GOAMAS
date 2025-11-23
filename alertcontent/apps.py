from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AlertcontentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alertcontent'
    verbose_name = '告警内容'

    def ready(self):
        from . import signals
        post_migrate.connect(signals.create_custom_permissions)
