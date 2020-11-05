from django.db import models
from django.contrib.postgres.fields import ArrayField

from .helpers import return_encoded_list


class Question(models.Model):

    text = models.CharField(max_length=255)
    img_url = models.URLField(null=False, blank=False)  # each question must have a image .
    hint = models.CharField(max_length=255)
    answer = ArrayField(models.CharField(max_length=255, blank=False))
    close_answers = ArrayField(models.CharField(max_length=255))

    def save(self, *args, **kwargs):
        self.answer = return_encoded_list(self.answer)
        self.close_answers = return_encoded_list(self.close_answers)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.text
