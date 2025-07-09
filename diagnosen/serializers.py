from rest_framework import serializers
from .models import Diagnosis
from icd.serializers import ICDSerializer

class DiagnosisSerializer(serializers.ModelSerializer):
    icd_code_detail = ICDSerializer(source='icd_code', read_only=True)
    
    class Meta:
        model = Diagnosis
        fields = ['id', 'title', 'icd_code', 'icd_code_detail']
        
class DiagnosisListSerializer(serializers.ModelSerializer):
 
    icd_code_text = serializers.CharField(source='icd_code.code', read_only=True)
    
    class Meta:
        model = Diagnosis
        fields = ['id', 'title', 'icd_code', 'icd_code_text']