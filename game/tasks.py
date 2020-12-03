from users.models import User
from django.db import transaction
from celery import shared_task


@shared_task
def increase_user_xp(**kwargs):
    user_id = kwargs.get('user_id', None)
    if user_id:
        with transaction.atomic():
            try:
                user = User.objects.get(id=user_id)
                if user.question_id > 14:
                    return None
                old_xp = user.xp
                new_xp = old_xp + 10
                if new_xp <= 100:
                    user.xp = new_xp
                    user.save()
                    return f"Increased XP of user {user.id} from {old_xp} to {new_xp}."
                elif new_xp > 100 and old_xp > 90:
                    user.xp = 100
                    user.save()
                    return f"Increased XP of user {user.id} from {old_xp} to 100."
                else:
                    return f"User {user.id} has {old_xp}, which is more than the cap."
            except User.DoesNotExist:
                pass
    return None
