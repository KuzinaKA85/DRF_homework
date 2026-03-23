from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """Сериализатор для платежей"""

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["user", "session_id", "link", "payment_date"]


class UserSerializer(ModelSerializer):
    """Сериализатор для пользователя с историей платежей"""

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone_number",
            "avatar",
            "country",
            "payments",
            "password",
        ]
