web: gunicorn jobtracker.wsgi --log-file -
worker: celery -A jobtracker worker --loglevel=info
beat: celery -A jobtracker beat --loglevel=info