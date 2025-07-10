from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Diagnosis
from .serializers import DiagnosisSerializer

class DiagnosisPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.select_related('icd_code').all()
    serializer_class = DiagnosisSerializer
    pagination_class = DiagnosisPagination
    
    def get_queryset(self):
        queryset = Diagnosis.objects.select_related('icd_code').all()
        code = self.request.query_params.get('code', None)
        name = self.request.query_params.get('name', None)
        
        if code or name:
            # Start with empty Q object
            q_objects = Q()

            
            # Add code filter if provided
            if code:
                q_objects &= Q(icd_code__code__icontains=code)
            
            # Add name filter if provided  
            if name:
                q_objects &= Q(title__icontains=name)
            
            queryset = queryset.filter(q_objects)
        
        return queryset.order_by('id')