from __future__ import absolute_import

import os
import django

from celery import Celery
from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enigma7_backend.settings')
django.setup()

app = Celery('enigma7_backend')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)