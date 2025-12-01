FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=stripeTestTask.settings
RUN python manage.py collectstatic --noinput
ENTRYPOINT python manage.py makemigrations && python manage.py migrate && gunicorn --bind=:80 stripeTestTask.wsgi
