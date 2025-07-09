from django.db import models
from icd.models import ICDCode

class Diagnosis(models.Model):
    title = models.CharField(max_length=255)
    icd_code = models.ForeignKey(ICDCode, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} ({self.icd_code.code})"    
  