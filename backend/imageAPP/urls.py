from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

# Importación de las clases de Views.py
from .views import ImageUpload, ImageDetail, TokenObtainPairView
from . import views

urlpatterns = [
    # Primer url para obtener el token con nuestro Usuario
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Segunda url para refrescar el token cuando se expire
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URLs para obtener las imágenes
    path('api/images/', ImageUpload.as_view(), name='image_upload'),
    path('api/images/<int:pk>/', ImageDetail.as_view(), name='image_detail'),
]