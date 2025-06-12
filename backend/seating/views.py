from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response 
from django.contrib.auth.models import User
from .models import Student, SeatLayout, Seat
from .serializers import StudentSerializer, UserSerializer, SeatLayoutSerializer, SeatSerializer
import random
class StudentViewSet(viewsets.ModelViewSet):
    # このビューが扱うデータ（原則）
    queryset = Student.objects.all()
    # 使用するシリアライザー
    serializer_class = StudentSerializer
    # アクセス権限：ログインしているユーザーのみ許可
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        このビューセットは、認証されたユーザーに関連する生徒のみを返すようにします。
        """
        return self.request.user.student_set.all()
    
    # ↓ このメソッドを追加します！
    def perform_create(self, serializer):
        """
        新しい生徒を作成する際に、リクエストしてきたユーザーを自動的に紐付けます。
        """
        serializer.save(user=self.request.user)

class UserCreateView(generics.CreateAPIView):
    """
    ユーザー新規作成のためのAPIビュー。
    誰でもアクセス可能。
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # 誰でもアクセスできるように設定

class SeatLayoutViewSet(viewsets.ModelViewSet):
    """
    座席表レイアウトの表示、作成、更新、削除を行うためのAPIビュー。
    """
    queryset = SeatLayout.objects.all()
    serializer_class = SeatLayoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        自分（ログインしているユーザー）が作成した座席表のみを返す。
        """
        return self.request.user.seatlayout_set.all()
    
   # SeatLayoutViewSet の中の shuffle メソッドを、以下に書き換えます

    @action(detail=True, methods=['post'])
    def shuffle(self, request, pk=None):
        """
        この座席表の席替えを実行するカスタムアクション。
        前回最前列だった生徒は、今回最前列に配置されないようにする。
        """
        seat_layout = self.get_object()
        
        # 1. 生徒と座席を準備
        all_students = list(Student.objects.filter(user=request.user))
        active_seats = list(seat_layout.seats.filter(is_active=True))

        if len(all_students) > len(active_seats):
            return Response({'error': '生徒数が座席数を超えています。'}, status=400)

        # 2. 生徒と座席をグループ分け
        veterans = [s for s in all_students if s.last_seated_row == 1]
        others = [s for s in all_students if s.last_seated_row != 1]
        
        front_row_seats = [seat for seat in active_seats if seat.row == 0]
        other_seats = [seat for seat in active_seats if seat.row != 0]

        if len(veterans) > len(other_seats):
            return Response({'error': '前回最前列だった生徒の数が多すぎて、全員を後方に配置できません。'}, status=400)

        # 3. グループごとにシャッフル
        random.shuffle(veterans)
        random.shuffle(others)
        random.shuffle(front_row_seats)
        random.shuffle(other_seats)

        # 4. 席替えロジック
        # まず、全ての座席を一旦空席にする
        seat_layout.seats.update(student=None)
        
        assigned_seats = []
        
        # A: 前回最前列だった生徒を、今回最前列"以外"の席に割り当てる
        for student in veterans:
            seat = other_seats.pop()
            seat.student = student
            assigned_seats.append(seat)

        # B: それ以外の生徒を、残りの全ての席に割り当てる
        remaining_students = others
        remaining_seats = front_row_seats + other_seats # Aで使われなかった席も含む
        random.shuffle(remaining_seats)
        
        for student in remaining_students:
            if not remaining_seats: break
            seat = remaining_seats.pop()
            seat.student = student
            assigned_seats.append(seat)
        
        # 5. データベースを更新
        # 席の割り当てを更新
        Seat.objects.bulk_update([s for s in assigned_seats if s.student is not None], ['student'])
        
        # 割り当てられた生徒の履歴(last_seated_row)を更新
        for seat in assigned_seats:
            student_to_update = seat.student
            if student_to_update:
                if seat.row == 0:
                    student_to_update.last_seated_row = 1 # 最前列に座った
                else:
                    student_to_update.last_seated_row = 2 # 最前列以外に座った
                student_to_update.save() # 1件ずつ更新

        # 6. 結果を返す
        serializer = self.get_serializer(seat_layout)
        return Response(serializer.data)
class SeatViewSet(viewsets.ModelViewSet):
    """
    個々の座席の情報を更新するためのAPIビュー。
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer # 既存のSeatSerializerを再利用します
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        自分（ログインしているユーザー）が所有する座席表に含まれる座席のみを返すように、
        セキュリティのためにデータをフィルタリングします。
        """
        return Seat.objects.filter(layout__user=self.request.user)