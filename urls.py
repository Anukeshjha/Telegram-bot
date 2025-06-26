from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home_view, api_docs_view, PublicDataViewSet, ProtectedDataViewSet, UserViewSet
from .views import register_user_view 
from .views import login_view, dashboard_view, logout_view
from .views import telegram_users_view

router = DefaultRouter()
router.register(r'public', PublicDataViewSet, basename='public')
router.register(r'protected', ProtectedDataViewSet, basename='protected')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', home_view, name='home'),  # Home page
    path('api/docs/', api_docs_view, name='api-docs'),  # Documentation
    path('register/', register_user_view, name='register-user'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('telegram-users/', telegram_users_view, name='telegram-users'),
    path('logout/', logout_view, name='logout'),
    path('api/', include(router.urls)),  # API endpoints
]