from django.urls import path
from course import views


urlpatterns = [
    path('course/create/', views.CourseAPI.as_view()),
    path('course/delete/', views.CourseAPI.as_view()),
    path('course/update/', views.CourseAPI.as_view()),
    path('course/list/', views.CourseAPI.as_view()),
    path('course/get/', views.CourseAPI.as_view()),
    path('lecture/create/', views.LectureAPI.as_view()),
    path('lecture/delete/', views.LectureAPI.as_view()),
    path('lecture/get/', views.LectureAPI.as_view()),
    path('lecture/list/', views.LectureAPI.as_view()),
    path('lecture/update/', views.LectureAPI.as_view()),
    path('lecture/count/', views.LectureAPI.as_view()),
    path('format/list/', views.FormatAPI.as_view()),
    path('genre/list/', views.GenreAPI.as_view()),
    path('comment/delete/', views.CommentAPI.as_view()),
    path('comment/update/', views.CommentAPI.as_view()),
    path('comment/list/', views.CommentAPI.as_view()),
    path('evaluation/list/', views.EvaluationAPI.as_view()),
    path('selection/create/', views.SelectionAPI.as_view()),
    path('selection/delete/', views.SelectionAPI.as_view()),


    path('getCourseById/', views.CourseAPI.as_view()),
]
