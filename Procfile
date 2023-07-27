web: gunicorn app.wsgi --log-file -
worker: celery -A app worker --loglevel=info
beat: celery -A app beat --loglevel=info
