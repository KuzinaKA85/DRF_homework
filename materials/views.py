from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from yaml import serialize

from materials.models import Course, Lesson, Subscription
from materials.pagination import MyPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner, IsNotModer


class CourseViewSet(ModelViewSet):
    """ViewSet-класс для курсов"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination

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

    def get(self, request):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class LessonListAPIView(generics.ListAPIView):
    """Список уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination


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


class SubscriptionAPIView(APIView):
    """API для управления подпиской на курс"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response({"error": "Не указан ID курса"}, status=400)

        course = get_object_or_404(Course, id=course_id)

        # Проверяем, есть ли подписка
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            # Если есть - удаляем
            subscription.delete()
            message = "Подписка удалена"
            is_subscribed = False
        else:
            # Если нет - создаем
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"
            is_subscribed = True

        return Response(
            {
                "message": message,
                "is_subscribed": is_subscribed,
                "course_id": course.id,
                "course_title": course.title_course,
            }
        )
