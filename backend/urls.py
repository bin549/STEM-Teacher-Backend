from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.authtoken')),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include('users.urls')),
    path('api/', include('course.urls')),
    path('api/', include('homework.urls')),
    path('api/', include('upload.urls')),
]
