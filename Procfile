release: python manage.py migrate && python manage.py seed
web: gunicorn devconnect.wsgi:application --log-file -