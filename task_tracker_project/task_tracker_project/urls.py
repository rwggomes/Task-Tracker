from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from task_app.views import TaskViewSet, FileUploadView
from django.http import HttpResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from task_app.views import UserRegistrationView
from task_app import views 
from django.shortcuts import render

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)

def home(request):
    return render(request, 'home.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='Home'),
    path('', home),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/', include(router.urls)),
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
 

# JWT auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

