from django.urls import include, path

app_name = "core"


urlpatterns = [
    path(
        "v1/",
        include("core.api.urls.v1_urls"),
        name="v1",
    ),
]
