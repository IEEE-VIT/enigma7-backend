from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, unique=True)
    points = models.IntegerField(default=0, db_index=True)
    question_answered = models.IntegerField(default=0)
    no_of_hints_used = models.IntegerField(default=0)
    no_of_attempts = models.IntegerField(default=0)
    question_id = models.IntegerField(default=1)
    xp = models.IntegerField(default=0, null=False, blank=False)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class UserStatus(models.Model):

    user = models.OneToOneField(User, related_name='user_status', on_delete=models.CASCADE)
    hint_used = models.BooleanField(default=False)
    hint_powerup = models.BooleanField(default=False)
    skip_powerup = models.BooleanField(default=False)
    accept_close_answer = models.BooleanField(default=False)
    last_answered_ts = models.DateTimeField(null=True, db_index=True)
    first_timestamp = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username


class Logging(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0, db_index=True)
    no_of_hints_used = models.IntegerField(default=0)
    no_of_attempts = models.IntegerField(default=0)
    question_id = models.IntegerField(default=1)
    timestamp = models.DateTimeField(null=True)
    xp = models.IntegerField(default=0, null=False, blank=False)
    hint_used = models.BooleanField(default=False)
    hint_powerup = models.BooleanField(default=False)
    skip_powerup = models.BooleanField(default=False)
    accept_close_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class UserOutreach(models.Model):
    OUTREACH_CHOICES = (
        ('Instagram', 'Instagram'),
        ('Twitter', 'Twitter'),
        ('Facebook', 'Facebook'),
        ('Word of mouth', 'Word of mouth'),
        ('WhatsApp', 'WhatsApp'),
        ('Reddit', 'Reddit'),
        ('E-Mail', 'E-Mail'),
        ('Other', 'Other')
    )
    YEAR_CHOICES = (
        (2020, 2020),
        (2021, 2021),
        (2022, 2022),
        (2023, 2023),
        (2024, 2024)
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    outreach = models.CharField(max_length=13, null=False, choices=OUTREACH_CHOICES)
    is_college_student = models.BooleanField(null=False)
    year = models.IntegerField(null=True, blank=True, choices=YEAR_CHOICES)

    def __str__(self):
        return self.user.email
