import uuid
import os
from django.db import models
from users.models import Profile
from course.models import Entity


class Assignment(models.Model):

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    intro = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Entity, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s' % self.intro


class Execution(models.Model):

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    score = models.IntegerField(null=True)
    finish_time = models.DateTimeField(null=True)
    is_excellent = models.BooleanField(default=False)
    content_text = models.CharField(null=True, max_length=2000)
    homework = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s' % self.id