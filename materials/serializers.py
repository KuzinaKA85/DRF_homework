from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from users.models import User


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone_number", "avatar", "country"]

