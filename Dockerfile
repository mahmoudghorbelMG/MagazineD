FROM python:3.11.2
RUN mkdir /app
WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install -y vim

WORKDIR /app

RUN python -m pip install -r requirements.txt
RUN pip install django-recaptcha --no-cache-dir
EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000