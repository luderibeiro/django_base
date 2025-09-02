from django.urls import include, path

app_name = "core"


urlpatterns = [
    path(
        "v1/",
        include("core.api.v1.urls"),
        name="v1",
    ),
]
