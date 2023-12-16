from django.apps import AppConfig


class ExampleConfig(AppConfig):
    verbose_name = "Приложение пример"  # название приложения в админке
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'example'
