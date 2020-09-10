from celery import shared_task
from celery import Celery

from users.models import User

@shared_task
def xp_generation():
    users = User.objects.exclude(first_attempt = None)
    for user_obj in users:
        user_obj.xp += 10
        user_obj.save()