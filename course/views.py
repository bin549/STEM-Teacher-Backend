import datetime
import random
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Entity, Genre, Lecture, Format
from users.models import Profile
from .serializers import CourseSerializer, LectureSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from django.db.models import Q


class CourseAPI(APIView):

    def get(self, request, format=None):
        if request.query_params.__contains__('id'):
            course = Entity.objects.get(Q(id=request.query_params["id"]))
            serializer = CourseSerializer(course, many=False)
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
            course.is_visible = request.data['status']
            course.save()
            return Response(1)
        except Exception:
            return Response(0)

    def delete(self, request, format=None):
        try:
            course = Entity.objects.get(Q(id=request.data['ids'][0]))
            # selections = Selection.objects.filter(Q(course=course.id))
            # wishlists = Wishlist.objects.filter(Q(course=course.id))
            # lectures = Lecture.objects.filter(Q(course=course.id))
            # selections.delete()
            # wishlists.delete()
            # lectures.delete()
            # course.delete()
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
