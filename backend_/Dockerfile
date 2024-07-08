FROM python:3.12

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY backend /app/backend

WORKDIR /app/backend
RUN python manage.py migrate

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 & celery -A backend worker --loglevel=info"]

