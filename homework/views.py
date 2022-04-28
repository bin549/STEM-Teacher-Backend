from django.shortcuts import render
from .models import Assignment, Execution, Media, MediaType, ExecutionStar
from .serializer import ActivitySerializer, ExecutionSerializer, MediaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from course.models import Entity, Selection
from users.models import Profile
import datetime


class AssignmentAPI(APIView):

    def get(self, request, format=None):
        if request.query_params.__contains__('selectedCourse'):
            assignments = Assignment.objects.all()
            assignments = assignments.filter(Q(course=request.query_params['selectedCourse']))
            serializer = ActivitySerializer(assignments, many=True)
            return Response(serializer.data)
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

    def put(self, request, format=None):
        activity = Assignment.objects.get(Q(id=request.query_params["id"]))
        activity.intro = request.query_params['intro']
        activity.description = request.query_params['description']
        activity.save()
        return Response(1)

    def delete(self, request, format=None):
        activity = Assignment.objects.get(Q(id=request.query_params['id']))
        executions = Execution.objects.filter(Q(homework=request.query_params['id']))
        for execution in executions:
            medias = Media.objects.filter(Q(execution=execution.id))
            executionStars = ExecutionStar.objects.filter(Q(execution=execution.id))
            if medias.exists():
                medias.delete()
            if executionStars.exists():
                executionStars.delete()
            execution.delete()
        activity.delete()
        return Response(1)


class ExecutionAPI(APIView):

    def get(self, request, format=None):
        if request.query_params.__contains__('is_done'):
            if request.query_params["is_done"] == "true":
                executions = Execution.objects.filter(Q(homework=request.query_params["id"]))
                print(1)
                executions = executions.exclude(Q(finish_time=None))
                return Response(len(executions))
            else:
                executions = Execution.objects.filter(Q(homework=request.query_params["id"]) & Q(finish_time=None))
                print(2)
                return Response(len(executions))
        elif request.query_params.__contains__('score'):
            execution = Execution.objects.get(Q(id=request.query_params["id"]))
            serializer = ExecutionSerializer(execution, many=False)
            return Response(serializer.data)
        elif request.query_params.__contains__('id'):
            executions = Execution.objects.filter(Q(homework=request.query_params["id"]))
            serializer = ExecutionSerializer(executions, many=True)
            return Response(serializer.data)
        elif request.query_params.__contains__('is_excellent'):
            courses = Entity.objects.filter(Q(owner=request.query_params["owner_id"]))
            excellent_executions = []
            for course in courses:
                assignments = Assignment.objects.filter((Q(course=course.id)))
                for assignment in assignments:
                    executions = Execution.objects.filter(Q(homework=assignment.id) & Q(is_excellent=True))
                    if executions.exists():
                        for execution in executions:
                            serializer = ExecutionSerializer(execution, many=False)
                            excellent_executions.append(serializer.data)
            return Response(excellent_executions)
        else:
            executions = Execution.objects.all()
            serializer = ExecutionSerializer(executions, many=True)
            return Response(serializer.data)

    def put(self, request, format=None):
        execution = Execution.objects.get(Q(id=request.data['id']))
        execution.appraise_star = request.data['appraise_star']
        execution.appraise_text = request.data['appraise_text']
        execution.save()
        return Response(1)


class MediaAPI(APIView):

    def get(self, request, format=None):
        execution = Execution.objects.get(Q(id=request.query_params["id"]))
        media_type = MediaType.objects.get(Q(name="Photo"))
        medias = Media.objects.filter(Q(execution=execution.id) & Q(type=media_type))
        serializer = MediaSerializer(medias, many=True)
        return Response(serializer.data)
