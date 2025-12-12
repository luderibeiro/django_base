from django.urls import include, path

urlpatterns = [
    path("v1/", include("cart.api.v1.urls")),
]
