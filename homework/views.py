from django.shortcuts import render
from .models import Assignment, Execution, Media, MediaType
from .serializer import ActivitySerializer, ExecutionSerializer, MediaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from course.models import Entity, Selection
import datetime


class AssignmentAPI(APIView):

    def get(self, request, format=None):
        if request.query_params.__contains__('selectedCourse'):
            assignments = Assignment.objects.all()
            assignments = assignments.filter(Q(course=request.query_params['selectedCourse']))
            serializer = ActivitySerializer(assignments, many=True)
        else:
            assignments = Assignment.objects.all()
            serializer = ActivitySerializer(assignments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        n_course = Entity.objects.get(Q(id=request.query_params['course']))
        assignment = Assignment()
        assignment.course = n_course
        assignment.intro = request.query_params['title']
        assignment.description = request.query_params['content']
        assignment.start_time = datetime.timedelta(days=30)
        assignment.end_time = datetime.timedelta(days=30)
        assignment.save()
        selections = Selection.objects.filter(Q(course=request.query_params['course']))
        for selection in selections:
            execution = Execution()
            execution.homework = assignment
            execution.user = selection.user
            execution.save()
        return Response(1)



class ExecutionAPI(APIView):

    def get(self, request, format=None):
        if request.query_params.__contains__('score'):
            execution = Execution.objects.get(Q(id=request.query_params["id"]))
            serializer = ExecutionSerializer(execution, many=False)
            return Response(serializer.data)
        elif request.query_params.__contains__('id'):
            executions = Execution.objects.filter(Q(homework=request.query_params["id"]))
            serializer = ExecutionSerializer(executions, many=True)
            return Response(serializer.data)
        else:
            executions = Execution.objects.all()
            serializer = ExecutionSerializer(executions, many=True)
            return Response(serializer.data)

    def put(self, request, format=None):
        execution = Execution.objects.get(Q(id=request.data['id']))
        execution.score = request.data['score']
        execution.save()
        return Response(1)


class MediaAPI(APIView):

    def get(self, request, format=None):
        execution = Execution.objects.get(Q(id=request.query_params["id"]))
        media_type = MediaType.objects.get(Q(name="Photo"))
        medias = Media.objects.filter(Q(execution=execution.id) & Q(type=media_type))
        serializer = MediaSerializer(medias, many=True)
        return Response(serializer.data)
