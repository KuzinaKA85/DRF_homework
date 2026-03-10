from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserDetailAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
]

# urlpatterns = [
#     path("login/", LoginView.as_view(template_name="login.html"), name="login"),
#     path(
#         "logout/",
#         LogoutView.as_view(template_name="logged_out.html"),
#         name="logout",
#     ),
# ]
