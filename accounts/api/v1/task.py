from celery import shared_task
import time

@shared_task
def send_email(Email):
    time.sleep(3)
    Email.send()
