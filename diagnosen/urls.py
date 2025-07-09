from rest_framework.routers import DefaultRouter
from .views import DiagnosisViewSet

router = DefaultRouter()
router.register(r'diagnoses', DiagnosisViewSet)

urlpatterns = router.urls