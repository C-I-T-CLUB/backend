release: python manage.py migrate
web: gunicorn citclub.wsgi:application --log-file - --log-level debug