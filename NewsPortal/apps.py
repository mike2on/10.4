from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NewsPortal'

    #def ready(self):
    #    from .signals import send_notifications, notify_about_new_post
