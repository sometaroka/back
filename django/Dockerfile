FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install djangorestframework
RUN pip install djangorestframework-simplejwt
RUN pip install django-cors-headers

ADD . /code/
