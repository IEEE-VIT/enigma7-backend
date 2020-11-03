from django.db import models
from django.contrib.postgres.fields import ArrayField


class Question(models.Model):

    text = models.CharField(max_length=255)
    img_url = models.URLField(null=False, blank=False)  # each question must have a image .
    hint = models.CharField(max_length=255)
    answer = ArrayField(models.CharField(max_length=255, blank=False))
    close_answers = ArrayField(models.CharField(max_length=255))

    def __str__(self):
        return self.text
