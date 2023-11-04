from django.shortcuts import render


# Create your views here.

from .models import MessagesModel ,translatedModel # モデル呼出

from rest_framework.generics import ListCreateAPIView  # API
from rest_framework import viewsets, filters
from .serializers import SampleSerializer,translateSerializer  # APIで渡すデータをJSON,XML変換
from .osaka_rules import translate_text_osaka

# 大阪弁の翻訳の呼び出し
# 複数の方言を使用する場合、受けとった変数によって切り替える場合urls.pyのurlを要変更
translate_text_osaka
class apiTest(ListCreateAPIView):
    # 対象とするモデルのオブジェクトを定義
    queryset = MessagesModel.objects.all()

    # APIがデータを返すためのデータ変換ロジックを定義
    serializer_class = SampleSerializer

    filter_fields = (
        "message_id",
        "message_data",
        "massege_date",
        "intnation",
        "user",
        "talk_id",
        "translated_data",
        
    )

class transTest(ListCreateAPIView):
    # 対象とするモデルのオブジェクトを定義
    queryset = translatedModel.objects.all()

    # APIがデータを返すためのデータ変換ロジックを定義
    serializer_class = translateSerializer

    filter_fields = (
        "translated_data",
        "message_data",
        
    )
    # 認証
    # permission_classes = []


