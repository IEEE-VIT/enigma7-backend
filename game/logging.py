from django.utils import timezone
from users.models import Logging


def logging(user):
    current_time = timezone.now()
    log_obj = Logging(user=user,
                      points=user.points,
                      no_of_hints_used=user.no_of_hints_used,
                      no_of_attempts=user.no_of_attempts,
                      question_id=user.question_id,
                      timestamp=current_time,
                      xp=user.xp,
                      hint_used=user.user_status.hint_used,
                      hint_powerup=user.user_status.hint_powerup,
                      skip_powerup=user.user_status.skip_powerup,
                      accept_close_answer=user.user_status.accept_close_answer
                      )

    log_obj.save()
    return None
