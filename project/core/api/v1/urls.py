from core.api.v1.views import auth, user
from django.urls import include, path

urlpatterns = [
    path("users/", user.UserCreateAPIView.as_view(), name="create-user"),
    path("users/list/", user.UserListAPIView.as_view(), name="user-list"),
    path(
        "users/alter_password/<uuid:pk>/",
        user.UserAlterPasswordAPIView.as_view(),
        name="user-alter-password",
    ),
    path(
        "users/<uuid:pk>/",
        user.UserRetrieveAPIView.as_view(),
        name="retrieve-user",
    ),
    path("login/", auth.LoginAPIView.as_view(), name="login"),
]

