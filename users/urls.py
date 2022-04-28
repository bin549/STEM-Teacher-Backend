from django.urls import path
from users import views

urlpatterns = [
    path('getUserByToken/', views.UserAPI.as_view()),
    path('getStudentByOwnerId/', views.StudentAPI.as_view()),
    path('getStudents/', views.StudentAPI.as_view()),
    path('getStudent/', views.StudentAPI.as_view()),
    path('getStudentCount/', views.StudentAPI.as_view()),
]
