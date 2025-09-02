from django.urls import include, path
from core.api.v1 import urls as core_api_v1_urls


app_name = "core"


urlpatterns = [
    path(
        "v1/",
        include(core_api_v1_urls),
        name="v1",
    ),
]
