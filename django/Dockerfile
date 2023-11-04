FROM python:3.6
ENV PYTHONUNBUFFERED 1

# ディレクトリを作成して移動
RUN mkdir /code
WORKDIR /code

# パッケージのアップデートと基本的なツールのインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

# requirements.txtをコピーしてpipパッケージをインストール
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 追加のpipパッケージをインストール
RUN pip install djangorestframework
RUN pip install django-filter

# MeCabと関連パッケージをインストール
RUN apt-get install -y \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8

# mecab-python3をインストール
RUN which mecab-config
RUN pip install mecab-python3

RUN pip install gspread
RUN pip install oauth2client
# 残りのコードをコピー
ADD . /code/

