from django.db import models
from django.contrib.auth.models import User # Django標準のユーザーモデルをインポート

# 生徒モデル
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # この生徒を管理するユーザー
    name = models.CharField(max_length=100) # 生徒の名前
    
    # 2回連続で最前列にしない機能のために、最後に座った列を記録するフィールド
    # 0は未着席、1は最前列、2は2列目...のように管理します
    last_seated_row = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True) # 作成日時
    updated_at = models.DateTimeField(auto_now=True) # 更新日時

    def __str__(self):
        return self.name
    
# 座席表全体のレイアウトを管理するモデル
class SeatLayout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="デフォルトの座席表")
    rows = models.IntegerField(default=6)
    cols = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # これが新規作成か、あるいは既存の更新かをチェック
        is_new = self.pk is None
        
        # もし既存の更新なら、行か列の数が変わったかをチェック
        if not is_new:
            original = SeatLayout.objects.get(pk=self.pk)
            if original.rows == self.rows and original.cols == self.cols:
                # 行も列も変わっていなければ、単純に保存して処理を終了
                super().save(*args, **kwargs)
                return

        # ここに到達した場合、それは「新規作成」か「行・列が変更された更新」のどちらか
        # どちらの場合でも、座席を再生成する必要がある

        # もし更新なら、まず関連する古い座席をすべて削除
        if not is_new:
            self.seats.all().delete()
        
        # SeatLayoutオブジェクト自体を保存 (新規作成の場合はここでIDが確定)
        super().save(*args, **kwargs)

        # 新しい行・列の数に基づいて、座席をゼロから再生成
        seats_to_create = []
        for r in range(self.rows):
            for c in range(self.cols):
                seats_to_create.append(Seat(layout=self, row=r, col=c))
        
        if seats_to_create:
            Seat.objects.bulk_create(seats_to_create)

# 個々の座席を管理するモデル
class Seat(models.Model):
    layout = models.ForeignKey(SeatLayout, on_delete=models.CASCADE, related_name='seats')
    row = models.IntegerField() # 座席の行番号 (0から)
    col = models.IntegerField() # 座席の列番号 (0から)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True) # 座っている生徒
    is_active = models.BooleanField(default=True) # この座席が使用可能か (削除された机はFalse)

    class Meta:
        # 同じレイアウト内で、同じ行・列の組み合わせはユニーク（一意）であるべき
        unique_together = ('layout', 'row', 'col')

    def __str__(self):
        return f"{self.layout.name} - (Row: {self.row}, Col: {self.col})"