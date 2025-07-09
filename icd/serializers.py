from rest_framework import serializers
from .models import ICDCode

class ICDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICDCode
        fields = '__all__'