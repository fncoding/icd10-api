from rest_framework import viewsets
from .models import ICDCode
from .serializers import ICDSerializer

class ICDViewSet(viewsets.ModelViewSet):
    queryset = ICDCode.objects.all()
    serializer_class = ICDSerializer