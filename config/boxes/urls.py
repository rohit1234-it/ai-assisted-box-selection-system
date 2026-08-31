from rest_framework.routers import DefaultRouter
from boxes.views import BoxViewSet

router = DefaultRouter()
router.register("boxes", BoxViewSet, basename="boxes")

urlpatterns = router.urls