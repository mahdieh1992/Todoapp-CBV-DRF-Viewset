import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Core.settings")
app = Celery("Core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "Delete_success_task": {
        "task": "accounts.tasks.delete_success_task",
        "schedule": crontab(minute="*/10"),
    },
}
