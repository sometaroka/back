FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install djangorestframework
RUN pip install django-filter

# add

# MeCabと関連パッケージをインストール
# パッケージのアップデートと基本的なツールのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev
    
RUN apt-get install -y \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8

# mecab-python3をインストール
RUN which mecab-config
RUN pip install mecab-python3

RUN pip install gspread
RUN pip install oauth2client

#####################

ADD . /code/
