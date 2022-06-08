from django.urls import path
from users import views

urlpatterns = [
    path('student/list/', views.StudentAPI.as_view()),
    path('user/list/', views.StudentAPI.as_view()),
    path('user/count/', views.StudentAPI.as_view()),


    path('getUserByToken/', views.UserAPI.as_view()),
    path('getStudent/', views.StudentAPI.as_view()),
]
