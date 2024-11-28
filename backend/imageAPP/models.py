from django.db import models

# Improtación de los modelos de Django
from django.contrib.auth.models import User
from django.db import models

# Modelo para la Imágen
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='original_images/')
    processed_image = models.ImageField(upload_to='processed_images/', null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    process_date = models.DateTimeField(null=True, blank=True)
    processing_details = models.JSONField(null=True, blank=True)