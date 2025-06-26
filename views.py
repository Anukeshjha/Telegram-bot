from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from core.serializers import UserSerializer
from core.tasks import send_welcome_email
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.models import TelegramUser

def register_user_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User created successfully!')
            return redirect('home')  # Redirect to home page after registration
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

@login_required
def telegram_users_view(request):
    telegram_users = TelegramUser.objects.select_related('user').all()
    print(telegram_users)  # Check console output when loading the page
    return render(request, 'telegram_users.html', {
        'telegram_users': telegram_users
    })
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html', {
        'user': request.user
    })

def logout_view(request):
    logout(request)
    return redirect('home')
def home_view(request):
        return render(request, 'home.html')

def api_docs_view(request):
        return render(request, 'api/docs.html')

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
        
    