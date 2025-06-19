# apps.py
from django.apps import AppConfig


class SeatingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seating'

    def ready(self):
        # 以前 signals.py にあったロジックを、ここに直接記述します
        from django.db.models.signals import post_save
        from django.dispatch import receiver
        from django.contrib.auth.models import User
        from .models import SeatLayout

        @receiver(post_save, sender=User)
        def create_default_seat_layout(sender, instance, created, **kwargs):
            if created:
                if not SeatLayout.objects.filter(user=instance).exists():
                    SeatLayout.objects.create(user=instance, name=f"{instance.username}の座席表")
                    print(f"Created default seat layout for new user: {instance.username}")
