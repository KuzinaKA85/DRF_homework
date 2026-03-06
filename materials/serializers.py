from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title_course",
            "preview",
            "description",
            "created_at",
            "updated_at",
            "is_published",
            "lesson_count",
            "lessons",
        ]

    def get_lesson_count(self, obj):
        return obj.lessons.count()
