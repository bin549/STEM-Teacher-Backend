import uuid
import os
from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Profile(models.Model):

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png")
    created_time = models.DateTimeField(auto_now_add=True)
    user_type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:

        db_table = "users_profile"
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ('-created_time',)

    def __str__(self):
        return str(self.username)

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url

    def get_image(self):
        if self.profile_image:
            return self.profile_image.url
        return ''
