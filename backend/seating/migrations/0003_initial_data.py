from django.db import migrations
import os

def create_initial_data(apps, schema_editor):
    # この処理が本番環境（Render）でのみ実行されるようにする
    if 'RENDER' in os.environ:
        User = apps.get_model('auth', 'User')
        SeatLayout = apps.get_model('seating', 'SeatLayout')

        # ↓↓↓【最重要】あなた自身の本番用アカウント情報に必ず変更してください ↓↓↓
        ADMIN_USERNAME = 'ray-admin'  # 例: あなたのユーザー名
        ADMIN_PASSWORD = 'daihuku0719' # ← 必ず変更！
        ADMIN_EMAIL = 'yama.game0719@gmail.com'      # ← あなたのメールアドレス
        # ↑↑↑【最重要】あなた自身の本番用アカウント情報に必ず変更してください ↑↑↑

        # 管理者ユーザーがまだ存在しない場合のみ作成
        if not User.objects.filter(username=ADMIN_USERNAME).exists():
            print(f"Creating superuser: {ADMIN_USERNAME}")
            admin_user = User.objects.create_superuser(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD
            )

            # 作成した管理者ユーザーに、デフォルトの座席表を作成
            if not SeatLayout.objects.filter(user=admin_user).exists():
                print(f"Creating default seat layout for {ADMIN_USERNAME}")
                SeatLayout.objects.create(
                    user=admin_user,
                    name=f"{ADMIN_USERNAME}の最初の座席表",
                    rows=6,
                    cols=5
                )

class Migration(migrations.Migration):

    dependencies = [
        ('seating', '0002_seatlayout_seat'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]