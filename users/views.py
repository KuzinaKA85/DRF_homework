from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.serializers import PaymentSerializer, UserSerializer
from users.models import Payment, User


class PaymentListAPIView(generics.ListAPIView):
    """Generic-класс для отображения списка платежей"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "paid_course__title_course",
        "paid_lesson__title_lesson",
        "payment_method",
    ]
    ordering_fields = ["payment_date", "amount"]
    ordering = ["-payment_date"]


# class UserDetailAPIView(generics.RetrieveAPIView):
#     """Generic-класс для отображения одного пользователя"""
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserViewSet(ModelViewSet):
    """ViewSet-класс для пользователей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)