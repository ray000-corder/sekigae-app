from django.contrib import admin
from .models import Student, SeatLayout, Seat  # 作成したStudentモデルをインポート

# Register your models here.
admin.site.register(Student) # Studentモデルを管理画面に登録
admin.site.register(SeatLayout)
admin.site.register(Seat) 
