from rest_framework.routers import DefaultRouter
from .views import ICDViewSet

router = DefaultRouter()
router.register(r'icd', ICDViewSet)

urlpatterns = router.urls