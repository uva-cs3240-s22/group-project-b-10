from django.apps import AppConfig


class StudyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'studyapp'

    def ready(self):
        from . import signals