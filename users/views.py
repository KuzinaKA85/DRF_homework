from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import (
    create_stripe_price,
    create_stripe_session,
    create_stripe_product,
)


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


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Generic-класс для создания платежа """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        # user автоматически берется из request.user
        payment = serializer.save(user=self.request.user)
        if payment.paid_course is None and payment.paid_lesson is None:
            raise ValidationError("Нужно выбрать курс или урок")
        elif payment.paid_course and payment.paid_lesson:
            raise ValidationError("Нужно выбрать либо курс, либо урок")

        # Создаем продукт в Stripe
        if payment.paid_course:
            product = create_stripe_product(payment.paid_course)
        else:
            product = create_stripe_product(payment.paid_lesson)
        # Создаем цену в Stripe
        price = create_stripe_price(stripe_product=product, amount=payment.amount)
        # Создаем сессию оплаты
        session_id, payment_link = create_stripe_session(price)
        # Сохраняем данные оплаты
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
