from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CustomUser(AbstractUser):
    last_action = models.DateTimeField(default=datetime.now())


class Like(models.Model):
    user = models.ForeignKey(CustomUser, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    create_at = models.DateField(auto_now_add=True)


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(max_length=200, verbose_name='post_name', null=False, default='title')
    text = models.TextField(null=False, blank=True)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.title