from django.urls import path
from . import views

urlpatterns = [
    path('getAssignment/', views.AssignmentAPI.as_view()),
    path('getExecution/', views.ExecutionAPI.as_view()),
    path('getExecutions/', views.ExecutionAPI.as_view()),
    path('updateExecution/', views.ExecutionAPI.as_view()),
    path('getExecutionImage/', views.MediaAPI.as_view()),
    path('getExecutionHomework/', views.AssignmentAPI.as_view()),
    path('createAssignment/', views.AssignmentAPI.as_view()),
    path('updateAssignment/', views.AssignmentAPI.as_view()),
    path('deleteAssignmnet/', views.AssignmentAPI.as_view()),
    path('getExecutionStatusCount/', views.ExecutionAPI.as_view()),
    path('getActivityLog/', views.LogAPI.as_view()),
]
