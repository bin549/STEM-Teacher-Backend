from rest_framework import serializers
from .models import Entity, Lecture, Format


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
            "serial_number",
        )


class LectureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = (
            "id",
            "index",
            "title",
            "created_time",
            "media",
            "format",
            "course",
            "is_preview",
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
