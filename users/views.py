from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

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


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
