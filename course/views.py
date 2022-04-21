import datetime
import random
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Entity, Genre, Lecture, Format, Selection, Wishlist
from users.models import Profile
from .serializers import CourseSerializer, LectureSerializer, GenreSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from django.db.models import Q
from homework.models import Assignment, Execution
from rest_framework import status


class CourseAPI(APIView):

    def get(self, request, format=None):
        print(request.query_params)
        print(request.query_params)
        if request.query_params.__contains__('id'):
            courses = Entity.objects.filter(Q(owner=request.query_params["id"]))
            if request.query_params.__contains__('genre'):
                courses = courses.filter(Q(genre=request.query_params["genre"]))
            if request.query_params.__contains__('status'):
                courses = courses.filter(Q(is_visible=request.query_params["status"]))
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        else:
            courses = Entity.objects.filter(Q(owner=request.query_params["0"]))
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        try:
            course = Entity()
            owner = Profile.objects.get(Q(id=request.data['owner']))
            genre = Genre.objects.get(Q(id=request.data['genre']))
            course.owner = owner
            course.genre = genre
            course.title = request.data['title']
            course.description = request.data['description']
            course.cover_img = request.data['cover']
            course.is_visible = request.data['status']
            course.created_time = datetime.timedelta(days=30)
            course.serial_number = int(random.random()*1000000)
            course.save()
            return Response(1)
        except Exception:
            return Response(0)

    def put(self, request, format=None):
        try:
            course = Entity.objects.get(Q(id=request.data['id']))
            if request.data['update'] == "row":
                course.title = request.data['title']
                course.description = request.data['description']
                genre = Genre.objects.get(Q(id=request.data['genre']))
                course.genre = genre
                if request.data['cover_name']:
                    course.cover_img = request.data['cover_name']
            if request.data['update'] == "status":
                course.is_visible = request.data['status']
            course.save()
            return Response(1)
        except Exception:
            return Response(0)

    def delete(self, request, format=None):
        try:
            course = Entity.objects.get(Q(id=request.data['ids'][0]))
            selections = Selection.objects.filter(Q(course=course.id))
            wishlists = Wishlist.objects.filter(Q(course=course.id))
            lectures = Lecture.objects.filter(Q(course=course.id))
            selections.delete()
            wishlists.delete()
            lectures.delete()
            course.delete()
            course.delete()
            return Response(1)
        except Exception:
            return Response(0)


class LectureAPI(APIView):

    def get(self, request, format=None):
        if request.query_params.__contains__('type'):
            format = Format.objects.get(Q(name=request.query_params["type"]))
            lectures = Lecture.objects.filter(Q(format=format.id))
            serializer = LectureSerializer(lectures, many=True)
            print(serializer.data)
            return Response(serializer.data)
        else:
            lectures = Lecture.objects.filter(Q(course=request.query_params["course_id"]))
            serializer = LectureSerializer(lectures, many=True)
            return Response(serializer.data)



class GenresAPI(APIView):

    def get(self, request, format=None):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)


class SelectionAPI(APIView):

    def post(self, request, format=None):
        try:
            course = Entity.objects.get(Q(id=request.data['course']))
            user = Profile.objects.get(Q(id=request.data['user']))
        except Exception:
            return Response('user Not Existed', status=status.HTTP_201_CREATED)
        try:
            Selection.objects.get(Q(user=request.data['user']) & Q(course=request.data['course']))
            return Response('Selection Existed', status=status.HTTP_201_CREATED)
        except Exception:
            selection = Selection()
            selection.user = user
            selection.course = course
            selection.select_time = datetime.timedelta(days=30)
            selection.save()
            # homeworks = Assignment.objects.filter(Q(course=course.id))
            # for homework in homeworks:
            #     execution = Execution()
            #     execution.homework = homework
            #     execution.user = user
            #     execution.save()
            return Response(1)


    def delete(self, request, format=None):
        selection = Selection.objects.get(Q(user=request.data["user"]) & Q(course=request.data['course']))
        homeworks = Assignment.objects.filter(Q(course=request.data['course']))
        # for homework in homeworks:
            # execution = Execution.objects.get(Q(user=request.data['user']) & Q(homework=homework.id))
            # print(execution)
            # print(execution)
            # execution.delete()
        # selection.delete()
        return Response(1)
