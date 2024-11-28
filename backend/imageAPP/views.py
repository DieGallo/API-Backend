# Libreria para guardar las fechas
from datetime import datetime
from django.shortcuts import render, redirect

# Librerias DRF para el manejo HTTP
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

# Libreria de DRF para la autenticación de Tokens
from rest_framework_simplejwt.views import TokenObtainPairView

# Libreria para tomar el modelo de User de Django
from django.contrib.auth.models import User

# Modelo de las imágenes en models.py
from .models import Image

# Serializadores
from .serializers import ImageSerializer, UserSerializer

# Librería de PILLOW para las fotografías
from PIL import Image as PILImage
import io

# Librerías para AWS Bucket S3
import boto3
from django.conf import settings
from botocore.exceptions import NoCredentialsError

# Clase para la creación de Usuario
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

# Clase para subir la imágen
class ImageUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    # Función para guardar la imágen
    def post(self, request, *args, **kwargs):
        # Guardamos la imágen, pero con el requerimiento del usuario
        file = request.data['file']
        image = Image.objects.create(user=request.user, original_image=file)
        
        # Procesamiento de la imagen
        self.process_image(image)
        processed_image_url = image.processed_image.url
        
        # Retornamos el status 201 de la imágen guardada
        return Response({
            'image': ImageSerializer(image).data,  # Datos de la imagen (puedes usar el serializer)
            'processed_image_url': processed_image_url  # URL de la imagen procesada
        }, status=status.HTTP_201_CREATED)

    # Procesamos la imágen con PILLOW
    def process_image(self, image):
        pil_image = PILImage.open(image.original_image)
        
        # Redimensionar la imagen Píxeles
        pil_image = pil_image.resize((800, 800))
        pil_image = pil_image.convert('L')
        
        # Declaramos el guardado con el formato y guardamos la imágen
        processed_io = io.BytesIO()
        pil_image.save(processed_io, format='JPEG', quality=85)
        processed_io.seek(0)

        # Agrgear extensión a la imágen procesada (Ruta)
        file_name = f"processed_{image.id}.jpg"
        image.processed_image.save(file_name, processed_io)
        image.process_date = datetime.now()
        image.processing_details = {'resize': '800x800', 'color': 'grayscale'}
        image.save()

        self.upload_bucket(processed_io, file_name)

    def upload_bucket(self, file, file_name):
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        try:
            s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file_name)
            print("Upload Successful")
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")

# Clase del detalle de la Imágen
class ImageDetail(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

class TokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)