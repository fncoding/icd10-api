from rest_framework import viewsets
from .models import Diagnosis
from .serializers import DiagnosisSerializer

class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
