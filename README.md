# Django Internship Assignment

## Setup Instructions

1. Create a Folder that name: telegram-bot

2. then open in cmd with this location: C:\Users\sachi\OneDrive\Desktop\Telegram-bot

3. then type code .

4. Step 1: Create Project & App
    bash
    # Create a virtual environment (optional but recommended)
    python -m venv venv

    .\venv\Scripts\activate   # Windows

    # Install Django
    pip install django

    # Create the Django project (automatically creates `config/`)
    django-admin startproject config .

    # Create the `core` app (automatically creates `core/`)
    python manage.py startapp core

5. Step 2: Add Required Files
    Now, manually create the remaining files:

    bash
    touch .env .gitignore README.md requirements.txt
    touch core/{serializers.py,urls.py,tasks.py,telegram_bot.py}

6.  in requirements.txt paste this: Django==4.2.0
    djangorestframework==3.14.0
    python-dotenv==1.0.0
    celery==5.3.0
    redis==4.5.5
    python-telegram-bot==20.3
    django-cors-headers==4.2.0

7. Install dependencies: `pip install -r requirements.txt`
8. Create a `.env` file with the following variables:
    "
    # Django Settings
    SECRET_KEY=g(k(mp04d&%aw^p_$tzn+3ref31$rk6n6lla17innc^_hr%b3l
    DEBUG=True  # Set to False in production

    # Database Configuration (PostgreSQL example)
    DB_NAME=telegram_bot
    DB_USER=django_user
    DB_PASSWORD=strong_password_123
    DB_HOST=localhost
    DB_PORT=5432

    # Celery Configuration
    CELERY_BROKER_URL=redis://localhost:6379/0

    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN=1234567890:YOUR_ACTUAL_TELEGRAM_BOT_TOKEN_FROM_BOTFATHER

    # Email Configuration (optional, for Celery email tasks)
    EMAIL_HOST=smtp.example.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=your_email@example.com
    EMAIL_HOST_PASSWORD=your_email_password
    EMAIL_USE_TLS=True 
    "

9. 1: Install and Run Redis on Windows
    Install Redis for Windows:

    Download Redis from Microsoft Archive

    Choose the latest release (e.g., Redis-x64-3.2.100.msi)

    Install it with default options

    Start Redis Service:

    Open Services (press Win+R and type services.msc)

    Find "Redis" service and start it

    Or run in command prompt:

    cmd
    redis-server  

10. in config/celery.py paste this:
    "import os
    from celery import Celery

    # Set the default Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    app = Celery('config')

    # Using a string here means the worker doesn't have to serialize
    # the configuration object to child processes.
    app.config_from_object('django.conf:settings', namespace='CELERY')

    # Load task modules from all registered Django apps.
    app.autodiscover_tasks() 
    "

11. then config/settings.py paste this: "
    import os
    from dotenv import load_dotenv
    from pathlib import Path

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv()

    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'

    ALLOWED_HOSTS = ['*']

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'rest_framework.authtoken',
        'core',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'config.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'config.wsgi.application'

    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    # Password validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Celery Configuration
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST_USER = 'noreply@yourdomain.com'
    # Internationalization
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = 'static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'

    # Default primary key field type
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',
        ],
    }

    # Celery Configuration
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    ROOT_URLCONF = 'config.urls' "

    then config/urls.py paste this: "
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('core.urls')),  # Include your app's URLs
        path('', include('core.urls')),      # Root URL
    ] 
    "

12. in core/apps.py paste this:
    "  
    from django.apps import AppConfig


    class CoreConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'core'
    "
    in models.py paste this: "from django.db import models
    from django.contrib.auth.models import User

    class TelegramUser(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
        telegram_username = models.CharField(max_length=100)
        chat_id = models.CharField(max_length=100)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.telegram_username 
    "

13.   in serializers.py paste this: 
    " 
    from rest_framework import serializers
    from django.contrib.auth.models import User
    from core.models import TelegramUser

    class UserSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True, required=True)
        
        class Meta:
            model = User
            fields = ['id', 'username', 'email', 'password']
            extra_kwargs = {
                'email': {'required': True},
                'username': {'required': True}
            }

        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user

    class TelegramUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = TelegramUser
            fields = ['telegram_username', 'created_at']
            read_only_fields = ['created_at'] " 

    in tasks.py paste this: " from celery import shared_task
    from django.core.mail import send_mail
    from django.conf import settings

    @shared_task(bind=True)
    def send_welcome_email(self, user_email, username):
        subject = 'Welcome to Our Platform'
        message = f'Hi {username}, thank you for registering with us!'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_email]
        
        send_mail(subject, message, email_from, recipient_list)
        return f"Email sent to {user_email}" 
        "

14. in telegram_bot.py paste this: 
    "
    import os
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
    from core.models import TelegramUser, User
    from django.conf import settings

    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        username = update.effective_user.username
        
        # Save to database
        TelegramUser.objects.update_or_create(
            chat_id=str(chat_id),
            defaults={'telegram_username': username}
        )
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Hello {username}! Your details have been saved."
        )

    def run_bot():
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.run_polling()
    "

15. in tests.py paste this: 
    "
    from celery import shared_task
    from django.core.mail import send_mail
    from django.conf import settings

    @shared_task
    def send_welcome_email(user_email, username):
        subject = 'Welcome to Our Platform'
        message = f'Hi {username}, thank you for registering with us!'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_email]
        
        send_mail(subject, message, email_from, recipient_list)
        return f"Email sent to {user_email}"
    "

16. in core/urls.py paste this: 
    "
    from django.urls import path, include
    from rest_framework.routers import DefaultRouter
    from core import views  # This import should work correctly

    router = DefaultRouter()
    router.register(r'public', views.PublicDataViewSet, basename='public')
    router.register(r'protected', views.ProtectedDataViewSet, basename='protected')
    router.register(r'users', views.UserViewSet, basename='user')

    urlpatterns = [
        path('', include(router.urls)),
    ]
    "

17. in core/views.py paste this:
    "
    from rest_framework import viewsets, permissions, status
    from rest_framework.response import Response
    from rest_framework.decorators import action
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token
    from rest_framework.permissions import IsAuthenticated
    from core.serializers import UserSerializer
    from core.tasks import send_welcome_email
    from django.contrib.auth import authenticate

    class PublicDataViewSet(viewsets.ViewSet):
        permission_classes = [permissions.AllowAny]
        
        def list(self, request):
            return Response({"message": "Welcome to Telegram Bot API"})
        
        @action(detail=False, methods=['get'])
        def public(self, request):
            return Response({"data": "This is public data"})

    class ProtectedDataViewSet(viewsets.ViewSet):
        permission_classes = [IsAuthenticated]
        
        def list(self, request):
            return Response({"data": f"Protected data for {request.user.username}"})

    class UserViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        
        @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
        def register(self, request):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Create user with hashed password
            user = User.objects.create_user(
                username=request.data['username'],
                email=request.data.get('email', ''),
                password=request.data['password']
            )
            
            # Create authentication token
            token = Token.objects.create(user=user)
            
            # Send welcome email via Celery
            send_welcome_email.delay(user.email, user.username)
            
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        
        @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
        def login(self, request):
            # Authenticate user
            user = authenticate(
                username=request.data.get('username'),
                password=request.data.get('password')
            )
            
            if not user:
                return Response(
                    {'error': 'Invalid username or password'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Get or create token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
    "

18. 1st implement mir=grations core: `python manage.py makemigrations core`
19. Run migrations: `python manage.py migrate`
20. collect staticfiles: `python manage.py collectstatic`
21. Create a superuser: `python manage.py createsuperuser`
username: admin
email: anukeshjha197@gmail.com
password: Admin@123

## Running the Project

22. Start Django server: `python manage.py runserver`
23. Start Celery worker: `celery -A config worker --loglevel=info`

## API Documentation

### Public Endpoint
- GET `/api/public/` - Accessible to everyone

### Protected Endpoints
- GET `/api/protected/` - Requires authentication (Token)
- POST `/api/users/register/` - User registration
- POST `/api/users/login/` - User login

### Telegram Bot
- Send `/start` command to your bot to register your Telegram username

Project Structure
text
telegram-bot/
├── config/              # Project settings
│   ├── settings.py      # Configuration
│   ├── urls.py          # Main URLs
│   └── celery.py        # Celery configuration
├── core/                # Main app
│   ├── migrations/      # Database migrations
│   ├── models.py        # Data models
│   ├── serializers.py   # API serializers
│   ├── tasks.py         # Celery tasks
│   ├── telegram_bot.py  # Bot handler
│   ├── urls.py          # App URLs
│   └── views.py         # API views
├── manage.py            # Django CLI
├── requirements.txt     # Dependencies
└── README.md            # This file