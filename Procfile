web: cd backend && gunicorn config.wsgi:application --workers 3 --bind 0.0.0.0:${PORT:-8000} --log-file -
release: cd backend && python manage.py migrate --noinput && python manage.py collectstatic --noinput
