FROM python:3.11.2
RUN mkdir /app
WORKDIR /app

RUN git clone --branch update https://github.com/mahmoudghorbelMG/MagazineD.git

RUN apt-get update
RUN apt-get install -y vim

WORKDIR /app/MagazineD

RUN python -m pip install -r requirements.txt
RUN pip install django-recaptcha --no-cache-dir

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000