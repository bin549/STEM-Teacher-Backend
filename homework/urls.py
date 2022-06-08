from django.urls import path
from . import views

urlpatterns = [
    path('assignment/create/', views.AssignmentAPI.as_view()),
    path('assignment/get/', views.AssignmentAPI.as_view()),
    path('assignment/update/', views.AssignmentAPI.as_view()),
    path('assignmnet/delete/', views.AssignmentAPI.as_view()),
    path('execution/update/', views.ExecutionAPI.as_view()),
    path('execution/get/', views.ExecutionAPI.as_view()),
    path('execution/list/', views.ExecutionAPI.as_view()),
    path('execution/count/', views.ExecutionAPI.as_view()),
    path('media/list/', views.MediaAPI.as_view()),
    path('log/get/', views.LogAPI.as_view()),


    path('getExecutionHomework/', views.AssignmentAPI.as_view()),
]
