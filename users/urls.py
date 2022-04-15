from django.urls import path
from users import views

urlpatterns = [
    path('getUserByToken/', views.UserAPI.as_view()),
    path('getStudentByOwnerId/', views.StudentAPI.as_view()),
]
