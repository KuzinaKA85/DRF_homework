from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner, IsNotModer


class CourseViewSet(ModelViewSet):
    """ViewSet-класс для курсов"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Создание: только НЕ модераторы
        if self.action == "create":
            return [IsAuthenticated(), IsNotModer()]
        # Удаление: только владелец
        elif self.action == "destroy":
            return [IsAuthenticated(), IsOwner()]
        # Редактирование: владелец ИЛИ модератор
        elif self.action in ["update", "partial_update"]:
            # Используем список разрешений - они работают как И
            return [IsAuthenticated(), IsOwner() or IsModer()]
        # Просмотр: все авторизованные
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Список уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание урока - только НЕ модераторы"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Обновление урока - владелец ИЛИ модератор"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        # Возвращаем список разрешений
        return [IsAuthenticated, IsOwner or IsModer]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока - только владелец"""

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
