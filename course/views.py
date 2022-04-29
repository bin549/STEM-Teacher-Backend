import datetime
import random
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Entity, Genre, Lecture, Format, Selection, Wishlist, Comment, Evaluation, Progress
from users.models import Profile
from .serializers import CourseSerializer, LectureSerializer, GenreSerializer, FormatSerializer, CommentSerializer, EvaluationSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from django.db.models import Q
from homework.models import Assignment, Execution
from rest_framework import status


class CourseAPI(APIView):

    def get(self, request, format=None):
        if request.query_params.__contains__('method'):
            course = Entity.objects.get(Q(id=request.query_params["id"]))
            serializer = CourseSerializer(course, many=False)
            return Response(serializer.data)
        elif request.query_params.__contains__('mode'):
            assignment = Assignment.objects.get(Q(id=request.query_params["id"]))
            course = Entity.objects.get(Q(id=assignment.course.id))
            serializer = CourseSerializer(course, many=False)
            return Response(serializer.data)
        elif request.query_params.__contains__('is_sort'):
            courses = Entity.objects.filter(Q(owner=request.query_params["id"])).order_by("-created_time")
            if len(courses) > 5:
                serializer = CourseSerializer(courses[0:5], many=True)
                return Response(serializer.data)
            else:
                serializer = CourseSerializer(courses, many=True)
                return Response(serializer.data)
        else:
            courses = Entity.objects.filter(Q(owner=request.query_params["id"]))
            if request.query_params.__contains__('genre'):
                courses = courses.filter(Q(genre=request.query_params["genre"]))
            if request.query_params.__contains__('status'):
                courses = courses.filter(Q(is_visible=request.query_params["status"]))
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
            course.price = request.data['price']
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
                course.price = request.data['price']
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
            course = Entity.objects.get(Q(id=request.data['id']))
            selections = Selection.objects.filter(Q(course=course.id))
            wishlists = Wishlist.objects.filter(Q(course=course.id))
            evaluations = Evaluation.objects.filter(Q(course=course.id))
            lectures = Lecture.objects.filter(Q(course=course.id))
            activities = Assignment.objects.filter(Q(course=course.id))
            if lectures.exists():
                for lecture in lectures:
                    comments = Comment.objects.filter(Q(lecture=lecture.id))
                    for comment in comments:
                        comment.delete()
                    lecture.delete()
            if activities.exists():
                for activity in activities:
                    executions = Execution.objects.filter(Q(homework=activity.id))
                    for execution in executions:
                        medias = Media.objects.filter(Q(execution=execution.id))
                        executionStars = ExecutionStar.objects.filter(Q(execution=execution.id))
                        if medias.exists():
                            medias.delete()
                        if executionStars.exists():
                            executionStars.delete()
                        execution.delete()
                    activity.delete()
            if evaluations.exists():
                for evaluation in evaluations:
                    evaluation.delete()

            if wishlists.exists():
                for wishlist in wishlists:
                    wishlist.delete()

            if selections.exists():
                for selection in selections:
                    selection.delete()
            course.delete()
            return Response(1)
        except Exception:
            return Response(0)


class GenreAPI(APIView):

    def get(self, request, format=None):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)


class LectureAPI(APIView):

    def get(self, request, format=None):
        if request.query_params.__contains__('type'):
            format = Format.objects.get(Q(name=request.query_params["type"]))
            lectures = Lecture.objects.filter(Q(format=format.id))
            serializer = LectureSerializer(lectures, many=True)
            print(serializer.data)
            return Response(serializer.data)
        elif request.query_params.__contains__('mode'):
            if (request.query_params["mode"] == "count"):
                lectures = Lecture.objects.filter(Q(course=request.query_params["course_id"]))
                return Response(len(lectures))
            else:
                lectures = Lecture.objects.filter(Q(course=request.query_params["id"]))
                lecture = lectures.get(Q(is_preview=True))
                serializer = LectureSerializer(lecture, many=False)
                return Response(serializer.data)
        elif request.query_params.__contains__('sort'):
            lectures = Lecture.objects.filter(Q(course=request.query_params["course_id"])).order_by(request.query_params['sort'])
            serializer = LectureSerializer(lectures, many=True)
            return Response(serializer.data)

        else:
            lectures = Lecture.objects.filter(Q(course=request.query_params["course_id"]))
            serializer = LectureSerializer(lectures, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        try:
            lecture = Lecture()
            course = Entity.objects.get(Q(id=request.data['course']))
            is_preview = False
            format = Format.objects.get(Q(id=request.data['format']))
            lecture.title = request.data['title']
            lecture.media = request.data['content']
            lecture.created_time = datetime.timedelta(days=30)
            lecture.course = course
            lecture.format = format
            lecture.is_preview = is_preview
            lecture.is_comment_check = True
            lecture.save()
            selections = Selection.objects.filter(Q(course=request.data["course"]))
            for selection in selections:
                progress = Progress()
                progress.user = selection.user
                progress.lecture = lecture
                progress.percent = 0.0
                progress.save()
            return Response(1)
        except Exception:
            return Response(0)

    def put(self, request, format=None):
        if request.query_params.__contains__('status'):
            lecture = Lecture.objects.get(Q(id=request.query_params['id']))
            lecture.is_preview = request.query_params["status"]
            lecture.save()
            return Response(1)
        return Response(1)

    def delete(self, request, format=None):
        try:
            lecture = Lecture.objects.get(Q(id=request.data['id']))
            comments = Comment.objects.filter(Q(lecture=lecture.id))
            progresses = Progress.objects.filter(Q(lecture=lecture.id))
            progresses.delete()
            for comment in comments:
                comment.delete()
            lecture.delete()
            return Response(1)
        except Exception:
            return Response(0)


class FormatAPI(APIView):

    def get(self, request, format=None):
        formats = Format.objects.all()
        serializer = FormatSerializer(formats, many=True)
        return Response(serializer.data)


class SelectionAPI(APIView):

    def post(self, request, format=None):
        try:
            user = Profile.objects.get(Q(id=request.data['user']))
        except Exception:
            return Response('user Not Existed', status=status.HTTP_201_CREATED)
        try:
            course = Entity.objects.get(Q(id=request.data['course']))
        except Exception:
            return Response('course Not Existed', status=status.HTTP_201_CREATED)
        try:
            Selection.objects.get(Q(user=request.data['user']) & Q(course=request.data['course']))
            return Response('Selection Existed', status=status.HTTP_201_CREATED)
        except Exception:
            selection = Selection()
            selection.user = user
            selection.course = course
            lectures = Lecture.objects.filter(Q(course=course.id))
            selection.select_time = datetime.timedelta(days=30)
            homeworks = Assignment.objects.filter(Q(course=course.id))
            for homework in homeworks:
                execution = Execution()
                execution.homework = homework
                execution.user = user
                execution.save()
            for lecture in lectures:
                progress = Progress()
                progress.user = user
                progress.lecture = lecture
                progress.percent = 0.0
                progress.save()
            selection.save()
            return Response(1)

    def delete(self, request, format=None):
        selection = Selection.objects.get(Q(user=request.data["user"]) & Q(course=request.data['course']))
        homeworks = Assignment.objects.filter(Q(course=request.data['course']))
        lectures = Lecture.objects.filter(Q(course=request.data['course']))
        for homework in homeworks:
            try:
                execution = Execution.objects.get(Q(user=request.data['user']) & Q(homework=homework.id))
                execution.delete()
            except:
                print("execution No Existed!")
        for lecture in lectures:
            progress = Progress.objects.get(Q(lecture=lecture.id) & Q(user=request.data["user"]))
            progress.delete()
            comments = Comment.objects.filter(Q(lecture=lecture.id) & Q(user=request.data["user"]))
            for comment in comments:
                comment.delete()
        selection.delete()
        return Response(1)


class CommentAPI(APIView):

    def get(self, request, format=None):
        comments = Comment.objects.filter(Q(lecture=request.query_params["id"]))
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def put(self, request, format=None):
        lecture = Lecture.objects.get(Q(id=request.query_params["id"]))
        lecture.is_comment_check = True
        lecture.save()
        return Response(1)

    def delete(self, request, format=None):
        comment = Comment.objects.get(Q(id=request.query_params["id"]))
        comment.delete()
        return Response(1)


class EvaluationAPI(APIView):

    def get(self, request, format=None):
        evalutions = Evaluation.objects.filter(Q(course=request.query_params["course_id"]))
        serializer = EvaluationSerializer(evalutions, many=True)
        return Response(serializer.data)
