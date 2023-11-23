from django.shortcuts import render


# Create your views here.

from .models import MessagesModel, TalksModel  # モデル呼出

from rest_framework.generics import ListCreateAPIView  # API
from rest_framework import viewsets, filters
from .serializers import SampleSerializer, TalkSerializer  # APIで渡すデータをJSON,XML変換


class apiGetTest(ListCreateAPIView):
    # 対象とするモデルのオブジェクトを定義
    # queryset = MessagesModel.objects.all()

    queryset = MessagesModel.objects.all().order_by('massege_date')

    # APIがデータを返すためのデータ変換ロジックを定義
    serializer_class = SampleSerializer

    filter_fields = (
        "message_id",
        "message_data",
        "massege_date",
        "intnation",
        "user",
        "talk_id",
    )

    # 認証
    # permission_classes = []


class getTalkRooms(ListCreateAPIView):
    queryset = TalksModel.objects.all()
    serializer_class = TalkSerializer
    filter_fields = ("talk_id",)
