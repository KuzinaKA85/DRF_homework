from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserCreateAPIView, UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    # path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
] + router.urls

# urlpatterns = [
#     path("login/", LoginView.as_view(template_name="login.html"), name="login"),
#     path(
#         "logout/",
#         LogoutView.as_view(template_name="logged_out.html"),
#         name="logout",
#     ),
# ]
