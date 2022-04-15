from django.urls import path
from . import views

urlpatterns = [
    path('getAssignment/', views.AssignmentAPI.as_view()),
    path('getExecution/', views.ExecutionAPI.as_view()),
]
