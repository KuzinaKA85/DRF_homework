from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """ViewSet-класс для курсов"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListAPIView(generics.ListAPIView):
    """Generic-класс для отображения списка уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Generic-класс для отображения одного урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    """Generic-класс для создания урока"""

    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Generic-класс для обновления урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Generic-класс для удаления урока"""

    queryset = Lesson.objects.all()
