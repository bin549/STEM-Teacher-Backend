from django.urls import path
from course import views


urlpatterns = [
    path('createCourse/', views.CourseAPI.as_view()),
    path('deleteCourse/', views.CourseAPI.as_view()),
    path('updateStatus/', views.CourseAPI.as_view()),
    path('getCourseByUserId/', views.CourseAPI.as_view()),
    path('getCourseById/', views.CourseAPI.as_view()),
    path('updateCourse/', views.CourseAPI.as_view()),
    path('getCourseId/', views.CourseAPI.as_view()),
    path('getGenres/', views.GenreAPI.as_view()),
    path('createLecture/', views.LectureAPI.as_view()),
    path('deleteLecture/', views.LectureAPI.as_view()),
    path('setPreviewLecture/', views.LectureAPI.as_view()),
    path('getPreviewLecture/', views.LectureAPI.as_view()),
    path('getLecturesByCourseId/', views.LectureAPI.as_view()),
    path('getLectureCount/', views.LectureAPI.as_view()),
    path('createSelection/', views.SelectionAPI.as_view()),
    path('deleteSelection/', views.SelectionAPI.as_view()),
    path('getFormats/', views.FormatAPI.as_view()),
    path('getComments/', views.CommentAPI.as_view()),
    path('deleteComments/', views.CommentAPI.as_view()),
    path('getEvaluations/', views.EvaluationAPI.as_view()),
    path('updateCommentCheckStatus/', views.CommentAPI.as_view()),
]
