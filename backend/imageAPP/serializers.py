# Importación de los serializadores
from rest_framework import serializers
# Improtamos el modelo de User
from django.contrib.auth.models import User
# Importamos el modelo que creamos de Image
from .models import Image

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'user', 'original_image', 'processed_image', 'upload_date', 'process_date', 'processing_details')
