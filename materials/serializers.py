from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import YouTubeValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeValidator(field="video_url")]
        read_only_fields = ["owner"]


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()

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
            "owner",
        ]
        read_only_fields = ["owner"]

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False
