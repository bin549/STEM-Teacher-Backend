from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from .models import Profile
from .serializers import UserSerializer
from django.db.models import Q
from course.models import Selection


class UserAPI(APIView):

    def get(self, request, format=None):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM authtoken_token WHERE key = %s", [request.query_params["token"]])
            row = cursor.fetchone()
        profile = Profile.objects.get(user=row[2])
        serializer = UserSerializer(profile, many=False)
        print(serializer)
        return Response(serializer.data)


class StudentAPI(APIView):

    def get(self, request, format=None):
        users = Profile.objects.all()
        users = users.filter(Q(user_type="aef1f51d-f13a-4e42-81b1-9f4e36523ad8"))
        if request.query_params.__contains__('selectedCourse'):
            selections = Selection.objects.filter(Q(course=request.query_params["selectedCourse"]))
            students = []
            for selection in selections:
                student = Profile.objects.get(Q(id=selection.user.id))
                students.append(student)
            serializer = UserSerializer(students, many=True)
            return Response(serializer.data)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
