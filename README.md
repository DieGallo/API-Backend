# Instrucciones API Backend
### Paso 1: Instalación de Librerías
Instalamos las librerías en nuestro VSCode.  
Las librerías las podemos encontrar en *requirements.txt*
~~~
 - pip install Django
 - pip install djangorestframework
 - pip install Pillow
 - pip install djangorestframework-simplejwt
 - pip install psycopg2-binary
# Librerías de AWS
 - pip install boto3
 - pip install django-storages
 - pip install botocore
~~~
### Paso 2: Implementación de AWS S3
Para que se pueda guardar en un **Bucket S3** tenemos que ingresar nuestras credenciales.  
Se recomienda crear un **.env** por seguridad de las credenciales de AWS
~~~
AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_S3_REGION_NAME = 'your-region' 
AWS_S3_SIGNATURE_VERSION = 's3v4' 
AWS_S3_FILE_OVERWRITE = False  
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
~~~
### Paso 3: Migración de bases de datos (PostgreSQL)
Migramos nuestra base de datos ingresando a **settings.py**  
Ingresamos nuestras credenciales.
~~~
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'api',
        'USER': 'root',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
~~~
Una vez ingresadas las credenciales escribimos la migración.
~~~
- python manage.py makemigrations
- python manage.py migrate
~~~
### Paso 4: Ejecutamos la API
Antes de ejecutar la API, creamos un super usuario ó con un Endpoint
~~~
- python manage.py createsuperuser
- py manage.py runserver
~~~
Abrimos Postman e ingresamos la colección del repositorio
**Paso 4.1: Obtener el Token**
- http://127.0.0.1:8000/api/token/
  - Seleccionamos método **POST**
  - Seleccionamos **Body**
  - Seleccionamos en **raw**
  - Ingresamos el siguiente **JSON**
    ~~~
    {
    "username": "diego", (Nombre del SuperUser)
    "password": "diego123" (Contraseña del SuperUser)
    }  
    ~~~
  - Nos retornará el Endpoint 2 Tokens - **Acceso** y **Refresh**:
    ~~~
    {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjgwNDIxNSwiaWF0IjoxNzMyNzE3ODE1LCJqdGkiOiIxMDVlYTdlYjk2YTI0YTA4YjlmMmY1NmJjOGNiM2VjZSIsInVzZXJfaWQiOjF9.L3dTmI84cAYMmh2J4DkIS_IH2j9eZJCMpHMLDujtrKI",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyNzE4MTE1LCJpYXQiOjE3MzI3MTc4MTUsImp0aSI6ImU4NmMyNmY5ZTY2ZTQzMTFiYmU0NDAxOWFiYmUzYTFlIiwidXNlcl9pZCI6MX0.peB-WqxUfaQXR9OwAU-twZS-EmjfqKwRxNxDbJRAfqk"
    }
    ~~~
**Paso 4.2: Subir imágen**
- http://127.0.0.1:8000/api/images/
    - Seleccionamos método **POST**
    - Selecconamos **Headers**
      - **Key:** Authorization
      - **Value:** Bearer + **AccessToken**
    - Regresamos a **Body**
      - Seleccionamos **form-data**
      - **Key:** file
        - El combobox seleccionamos **File**
      - **Value:** *Subimos nuestra imágen*
        - Presionamos en **New file from local machine**
        - Subimos la foto presionamos este ícono
          
          ![image](https://github.com/user-attachments/assets/0afbf390-dc71-49f0-9d98-02904125ee31)
      - Se cargará la imágen y presionamos en **Send**
    - Nos retornará el siguiente **JSON**
      ~~~
      {
        "image": {
             "id": 13,
             "user": 1,
             "original_image": "https://bucketpruebatecnicainbest.s3.amazonaws.com/media/original_images/mujer_CDWL3eh.jpg",
             "processed_image": "https://bucketpruebatecnicainbest.s3.amazonaws.com/media/processed_images/processed_13.jpg",
             "upload_date": "2024-11-28T19:45:08.924726Z",
             "process_date": "2024-11-28T13:45:08.961816Z",
             "processing_details": {
                 "resize": "800x800",
                 "color": "grayscale"
             }
         },
         "processed_image_url": "https://bucketpruebatecnicainbest.s3.amazonaws.com/media/processed_images/processed_13.jpg"
      }
      ~~~
    - Tendremos dos enlaces, **original_image** y **processed_image**
    - Podemos usar la combinación de teclas **Ctrl + Click** en cualquiera de estos enlaces.
    - Se nos mostrarán las fotos, la original y la procesada a escala de grises.
### Expiración de Token
En dado caso que se nos haya expirado el token vamos a utilizar el siguiente endpoint.  
Cuando obtenemos el token con http://127.0.0.1:8000/api/token/ nos entrega un refresh, se va a necesitar.
- http://127.0.0.1:8000/api/token/refresh/
  - Seleccionamos método **POST**
  - Seleccionamos **Body**
  - Seleccionamos **raw**
  - *Ingresamos nuestro Token refresh*
    ~~~
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjkwNTI0MiwiaWF0IjoxNzMyODE4ODQyLCJqdGkiOiJhZTBjNTY3ZWFmNzg0MzVjYmRlZmQ5MTI5MGFmZTY4YiIsInVzZXJfaWQiOjF9.sVDuJkkqGOeNps4Rrv7R3Qm5WG1ff8_dVLiUYokzCPA"
    }
    ~~~
  - Nos retornará en el Response un Token access vigente.
    ~~~
    {
     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyODIzODY1LCJpYXQiOjE3MzI4MTg4NDIsImp0aSI6ImMxNzczY2NmODE5YTRlYmNiNzMxZjAxNzNlMWQ3MWE2IiwidXNlcl9pZCI6MX0.ZhlavaHbi6kRoK08pRKk8x0HlzO-nCj1ciDvj8qmuoo"
    } 
    ~~~
### IMPORTANTE: Guardado de las imágenes.  
En donde se encuentra las directorios **backend** y **imageAPP** se nos creará una carpeta llamado **media**  
- backend
- imageAPP
- media
  - original_images
    - *fotos subidas*
  - processed_images
    - *fotos subidas a escala de grises*
 
#### En nuestro Bucket S3 se nos van a guardar las fotografías de igual manera que en el directorio de **media** en *VSCode*
![image](https://github.com/user-attachments/assets/dcfecb42-bb8e-4f2d-b2a8-593851ba4ed1)
