from celery import shared_task
from django.contrib.auth import get_user_model


@shared_task
def reset_daily_chats():
    User = get_user_model()
    User.objects.update(daily_chats=0)
