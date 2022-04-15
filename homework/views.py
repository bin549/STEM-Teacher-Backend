from django.shortcuts import render
from .models import Assignment, Execution
from .serializer import ActivitySerializer, ExecutionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class AssignmentAPI(APIView):

    def get(self, request, format=None):
        assignments = Assignment.objects.all()
        serializer = ActivitySerializer(assignments, many=True)
        return Response(serializer.data)


class ExecutionAPI(APIView):

    def get(self, request, format=None):
        executions = Execution.objects.all()
        serializer = ExecutionSerializer(executions, many=True)
        return Response(serializer.data)
