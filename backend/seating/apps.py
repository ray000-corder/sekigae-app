# apps.py
from django.apps import AppConfig


class SeatingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.seating'  # ← フルパスに変更

    def ready(self):
        from backend.seating import signals  # ← 安全な書き方
