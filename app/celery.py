from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Django 프로젝트의 설정을 위한 환경 변수 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery(
    'app',
    broker=f'redis://{os.getenv("REDIS_HOST")}:6379/0',
    backend=f'redis://{os.getenv("REDIS_HOST")}:6379/0',
)

# Django 프로젝트의 설정을 Celery에 사용
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django 앱의 모든 tasks.py 모듈을 찾아 task를 등록
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 매일 자정에 'reset_daily_chats' 작업을 실행
    'reset-every-midnight': {
        'task': 'user.tasks.reset_daily_chats',
        'schedule': crontab(hour=0, minute=0),
    },
}
