from rest_framework import serializers
from .models import Student, SeatLayout, Seat
from django.contrib.auth.models import User

# 1. Seat Serializer (新しい座席用のシリアライザー)
class SeatSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True, default=None)
    
    class Meta:
        model = Seat
        fields = ['id', 'row', 'col', 'student', 'student_name', 'is_active']

# 2. SeatLayout Serializer (新しい座席表用のシリアライザー)
class SeatLayoutSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = SeatLayout
        fields = ['id', 'name', 'rows', 'cols', 'created_at', 'seats']

# 3. User Serializer (既存のユーザー登録用)
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

# 4. Student Serializer (既存の生徒用)
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'last_seated_row', 'created_at']