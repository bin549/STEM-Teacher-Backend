from django.urls import path
from course import views


urlpatterns = [
    path('getCourseByUserId/', views.CourseAPI.as_view()),
    path('updateStatus/', views.CourseAPI.as_view()),
    path('createCourse/', views.CourseAPI.as_view()),
    path('deleteCourse/', views.CourseAPI.as_view()),
    path('getCourseById/', views.CourseAPI.as_view()),
    path('getLecturesByCourseId/', views.LectureAPI.as_view()),
]
