import datetime
import random
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Entity, Genre, Lecture, Format, Selection, Wishlist, Comment, Evaluation, Progress, History
from users.models import Profile
from .serializers import CourseSerializer, LectureSerializer, GenreSerializer, FormatSerializer, CommentSerializer, EvaluationSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from django.db.models import Q
from homework.models import Assignment, Execution
from rest_framework import status
from django.db import connection


class CourseAPI(APIView):

    def get(self, request, format=None):
        if request.query_params.__contains__('page'):
            courses = Entity.objects.filter(Q(owner=request.query_params["id"]))
            if request.query_params.__contains__('genre'):
                courses = courses.filter(Q(genre=request.query_params["genre"]))
            if request.query_params.__contains__('status'):
                courses = courses.filter(Q(is_visible=request.query_params["status"]))
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        elif request.query_params.__contains__('sort_by'):
            if request.query_params["sort_by"] == "count":
                courses = Entity.objects.filter(Q(owner=request.query_params["id"]))
                sorted_courses = []
                for course in courses:
                    selections = Selection.objects.filter(Q(course=course.id))
                    sorted_courses.append({"id": course.id, "title": course.title, "price": course.price, "count": len(selections)})
                length = len(sorted_courses)
                for i in range(length - 1):
                    least = i
                    for k in range(i + 1, length):
                        if sorted_courses[k]["count"] > sorted_courses[least]["count"]:
                            least = k
                    if least != i:
                        sorted_courses[least], sorted_courses[i] = (sorted_courses[i], sorted_courses[least])
                if len(courses) > 5:
                    sorted_courses = sorted_courses[0:5]
                return Response(sorted_courses)
            elif request.query_params["sort_by"] == "created_time":
                courses = Entity.objects.filter(Q(owner=request.query_params["id"])).order_by("-created_time")
                if len(courses) > 5:
                    courses = courses[0:5]
                serializer = CourseSerializer(courses[0:5], many=True)
                return Response(serializer.data)
        elif request.query_params.__contains__('method'):
            course = Entity.objects.get(Q(id=request.query_params["id"]))
            serializer = CourseSerializer(course, many=False)
            return Response(serializer.data)
        elif request.query_params.__contains__('mode'):
            assignment = Assignment.objects.get(Q(id=request.query_params["id"]))
            course = Entity.objects.get(Q(id=assignment.course.id))
            serializer = CourseSerializer(course, many=False)
            return Response(serializer.data)
        else:
            courses = Entity.objects.filter(Q(owner=request.query_params["id"]))
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
        print(request.data)
        course = Entity.objects.get(Q(id=request.data['id']))
        if "is_visible" in request.data:
            course.is_visible = request.data['is_visible']
        else:
            course.title = request.data['title']
            course.description = request.data['description']
            course.price = request.data['price']
            genre = Genre.objects.get(Q(id=request.data['genre']))
            course.genre = genre
            course.is_visible = genre
            if "cover_img" in request.data:
                course.is_visible = request.data['cover_img']
        course.save()
        return Response(1)


    def delete(self, request, format=None):
        try:
            course = Entity.objects.get(Q(id=request.data['id']))
            selections = Selection.objects.filter(Q(course=course.id))
            wishlists = Wishlist.objects.filter(Q(course=course.id))
            evaluations = Evaluation.objects.filter(Q(course=course.id))
            lectures = Lecture.objects.filter(Q(course=course.id))
            activities = Assignment.objects.filter(Q(course=course.id))
            print(1)
            if lectures.exists():
                for lecture in lectures:
                    comments = Comment.objects.filter(Q(lecture=lecture.id))
                    progresses = Progress.objects.filter(Q(lecture=lecture.id))
                    histories = History.objects.filter(Q(lecture=lecture.id))
                    for comment in comments:
                        comment.delete()
                    for progress in progresses:
                        progress.delete()
                    for history in histories:
                        history.delete()
                    lecture.delete()
            print(2)
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
            print(3)
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
            if request.query_params["mode"] == "count":
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
        index = 0
        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(index) FROM course_lecture WHERE course_id = %s", [request.data['course']])
            row = cursor.fetchone()
            index = row[0]
            if index is None:
                index = 0
            else:
                index += 1
        try:
            lecture = Lecture()
            course = Entity.objects.get(Q(id=request.data['course']))
            is_preview = False
            format = Format.objects.get(Q(id=request.data['format']))
            lecture.title = request.data['title']
            lecture.media = request.data['content']
            lecture.index = index
            lecture.created_time = datetime.timedelta(days=30)
            lecture.course = course
            lecture.format = format
            lecture.is_preview = is_preview
            lecture.is_comment_check = True

            # lecture.index = request.data['index']

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
        lecture = Lecture.objects.get(Q(id=request.data['id']))
        lecture.is_preview = request.data["is_preview"]
        lecture.save()
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
        lecture = Lecture.objects.get(Q(id=request.data["id"]))
        lecture.is_comment_check = True
        lecture.save()
        return Response(1)

    def delete(self, request, format=None):
        comment = Comment.objects.get(Q(id=request.data["id"]))
        comment.delete()
        return Response(1)


class EvaluationAPI(APIView):

    def get(self, request, format=None):
        evalutions = Evaluation.objects.filter(Q(course=request.query_params["course_id"]))
        serializer = EvaluationSerializer(evalutions, many=True)
        return Response(serializer.data)
