from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.dispatch import receiver
import os
import shutil


class Post(models.Model):
    title = models.CharField(max_length=1024)
    post_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    num_view = models.IntegerField(default=0)

    @property
    def content_path(self):
        return os.path.join(settings.MEDIA_ROOT, str(self.pk), "index.htm")

    def __unicode__(self):
        return self.title


@receiver(models.signals.post_delete, sender=Post)
def delete_post_folder(sender, instance, **kwargs):
    post_folder_path = os.path.join(settings.MEDIA_ROOT, str(instance.id))
    if os.path.isdir(post_folder_path):
        shutil.rmtree(post_folder_path)


class Tag(models.Model):
    name = models.CharField(max_length=1024)
    linked_posts = models.ManyToManyField(Post, related_name="tags", blank=True)