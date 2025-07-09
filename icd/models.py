from django.db import models

class ICDCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.code}: {self.description}"
   
