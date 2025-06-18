# apps.py
from django.apps import AppConfig


class SeatingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seating'

    def ready(self):
        # ↓ この書き方が正しいです
        import seating.signals
