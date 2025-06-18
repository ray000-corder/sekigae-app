from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import SeatLayout

@receiver(post_save, sender=User)
def create_default_seat_layout(sender, instance, created, **kwargs):
    """
    新しいユーザーが作成された(created=True)場合に、この関数が自動的に呼び出される
    """
    if created:
        # 念のため、すでにレイアウトが存在しないか確認
        if not SeatLayout.objects.filter(user=instance).exists():
            SeatLayout.objects.create(user=instance, name=f"{instance.username}の座席表")
            print(f"Created default seat layout for new user: {instance.username}")