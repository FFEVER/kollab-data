release: python manage.py migrate
release: python manage.py fetch_data
web: gunicorn recommender.wsgi
web: gunicorn recommender.wsgi --log-file -
