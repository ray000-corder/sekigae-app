from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
import random
from django.contrib.auth.models import User
from .models import Student, SeatLayout, Seat
from .serializers import StudentSerializer, UserSerializer, SeatLayoutSerializer, SeatSerializer

class SeatViewSet(viewsets.ModelViewSet):
    """
    個々の座席の情報を更新するためのAPIビュー。
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        自分（ログインしているユーザー）が所有する座席表に含まれる座席のみを返すように、
        セキュリティのためにデータをフィルタリングします。
        """
        return Seat.objects.filter(layout__user=self.request.user)

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
    
    # ↓↓↓ このメソッドを、もう一度追加してください！ ↓↓↓
    def perform_create(self, serializer):
        """
        新しい座席表を作成する際に、リクエストしてきたユーザーを自動的に紐付けます。
        """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def shuffle(self, request, pk=None):
        """
        この座席表の席替えを実行するカスタムアクション。
        前回最前列だった生徒は、今回最前列に配置されないようにする。
        """
        # ... (shuffleの中身は変更なし) ...
        seat_layout = self.get_object()
        all_students = list(Student.objects.filter(user=request.user))
        active_seats = list(seat_layout.seats.filter(is_active=True))
        if len(all_students) > len(active_seats):
            return Response({'error': '生徒数が座席数を超えています。'}, status=400)
        veterans = [s for s in all_students if s.last_seated_row == 1]
        others = [s for s in all_students if s.last_seated_row != 1]
        front_row_seats = [seat for seat in active_seats if seat.row == 0]
        other_seats = [seat for seat in active_seats if seat.row != 0]
        if len(veterans) > len(other_seats):
            return Response({'error': '前回最前列だった生徒の数が多すぎて、全員を後方に配置できません。'}, status=400)
        random.shuffle(veterans)
        random.shuffle(others)
        random.shuffle(front_row_seats)
        random.shuffle(other_seats)
        seat_layout.seats.update(student=None)
        assigned_seats = []
        for student in veterans:
            if not other_seats: break
            seat = other_seats.pop()
            seat.student = student
            assigned_seats.append(seat)
        remaining_students = others
        remaining_seats = front_row_seats + other_seats
        random.shuffle(remaining_seats)
        for student in remaining_students:
            if not remaining_seats: break
            seat = remaining_seats.pop()
            seat.student = student
            assigned_seats.append(seat)
        Seat.objects.bulk_update([s for s in assigned_seats if s.student is not None], ['student'])
        for seat in assigned_seats:
            student_to_update = seat.student
            if student_to_update:
                if seat.row == 0:
                    student_to_update.last_seated_row = 1
                else:
                    student_to_update.last_seated_row = 2
                student_to_update.save()
        serializer = self.get_serializer(seat_layout)
        return Response(serializer.data)


class UserCreateView(generics.CreateAPIView):
    # ... (変更なし)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class StudentViewSet(viewsets.ModelViewSet):
    # ... (変更なし)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return self.request.user.student_set.all()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)