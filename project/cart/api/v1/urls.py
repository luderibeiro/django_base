from cart.api.v1.views import CartViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", CartViewSet, basename="cart")

urlpatterns = router.urls
