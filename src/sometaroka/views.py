from django.shortcuts import render


# Create your views here.

from .models import MessagesModel  # モデル呼出

# from rest_framework.generics import ListCreateAPIView  # API
from rest_framework import viewsets, filters
from .serializers import SampleSerializer  # APIで渡すデータをJSON,XML変換


class apiTest(viewsets.ModelViewSet):
    # 対象とするモデルのオブジェクトを定義
    queryset = MessagesModel.objects.all()

    # APIがデータを返すためのデータ変換ロジックを定義
    serializer_class = SampleSerializer

    filter_fields = ("message_id", "massege_date", "user")

    # 認証
    # permission_classes = []
