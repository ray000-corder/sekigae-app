from django.apps import AppConfig


class SeatingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seating'

    def ready(self):
        import seating.signals # signals.pyをインポート