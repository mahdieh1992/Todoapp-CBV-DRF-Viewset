from celery import shared_task
import time
from mail_templated import EmailMessage
from Todo.models import Todo
from django_celery_results.models import TaskResult


@shared_task()
def send_email(template_name, *args, **kwargs):
    time.sleep(20)
    email = EmailMessage(template_name, *args, **kwargs)
    email.send()


@shared_task()
def count_Todo():
    return Todo.objects.count()


@shared_task()
def send_email_task(template_name=None, *args, **kwargs):
    time.sleep(20)
    Email = EmailMessage(
        "email/hello.tp1",
        {"token": "mahdieh"},
        "mohamadimahdieh70@gmil.com",
        ["ebrahimi.7diamonds@gmail.com"],
    )
    Email.send()


@shared_task()
def delete_success_task():
    task_object = TaskResult.objects.all()
    task_object.filter(status="SUCCESS").delete()
