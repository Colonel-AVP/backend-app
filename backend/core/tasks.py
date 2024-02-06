from celery import shared_task
from .models import Department
from django.core.mail import send_mail
import random


@shared_task
def get_department_count():
    queryset = Department.objects.all()
    department_count = queryset.count()
    return department_count


@shared_task(bind=True)
def department_exist_check(name):
    data = Department.objects.filter(name__iexact=name).exists()
    return data


def exponential_backoff(task_self):
    """
    Utility function to calculate backoff between retries.
    """
    minutes = task_self.default_retry_delay / 60
    rand = random.uniform(minutes, minutes * 1.3)
    return int(rand**task_self.request.retries) * 60


@shared_task(bind=True, max_retries=3, default_retry_delay=120)
def send_welcome_email(self, email):
    print(email)
    subject = "Welcome to Proem Sports"
    message = "Thank you for creating an account! You can access Organon"
    from_email = "sardar_ramesh@outlook.com"
    recipient_list = [email]
    result = send_mail(subject, message, from_email, recipient_list)
    print(result)
    return result


# @shared_task()
# def send_timetable_everyday(self):
#     subject = "Proem Sports - Weekly Timetable"
#     message = ""
#     from_email = "sardar_ramesh@outlook.com"
#     recipient_list = [email]
#     result = send_mail(subject, message, from_email, recipient_list)


@shared_task
def add(x, y):
    return x + y


@shared_task
def multiply(x, y):
    return x * y


@shared_task
def subtract(x, y):
    if isinstance(x, list):
        return [item - y for item in x]
    else:
        return x - y
