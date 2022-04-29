from rest_framework import serializers
from .models import Entity, Lecture, Format, Genre, Comment, Evaluation, Progress


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Entity
        fields = (
            "id",
            "title",
            "description",
            "cover_img",
            "created_time",
            "owner",
            "genre",
            "is_visible",
            "get_absolute_url",
            "get_image",
            "get_student_url",
            "price",
            "serial_number",
        )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = (
            "id",
            "name"
        )


class LectureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = (
            "id",
            "index",
            "title",
            "created_time",
            "cover_img",
            "media",
            "format",
            "course",
            "is_preview",
            "is_comment_check",
            "get_absolute_url",
            "get_media"
        )


class FormatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Format
        fields = (
            "id",
            "name",
        )


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "lecture",
            "content",
            "comment_time",
        )


class EvaluationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evaluation
        fields = (
            "id",
            "user",
            "course",
            "content",
            "evaluate_time",
        )


class ProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Progress
        fields = (
            "id",
            "user",
            "lecture",
            "percent",
        )
