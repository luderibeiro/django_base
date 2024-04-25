from core.api.v1.views import user
from django.urls import include, path

app_name = "core"

user = [
    path("user/list", user.UserListAPIView.as_view()),
    path(
        "user/alter_password/<int:pk>/",
        user.UserAlterPasswordAPIView.as_view(),
        name="user_alter_password",
    ),
]

urlpatterns = [
    path(
        "v1/",
        include("core.api.urls.v1_urls"),
        name="v1",
    ),
] + user
