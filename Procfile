release: python3 manage.py migrate
web: gunicorn likeestampa.wsgi --timeout 90 --preload --log-file -