from django.shortcuts import render


# Create your views here.

from .models import MessagesModel ,translatedModel # モデル呼出
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView  # API
from rest_framework import viewsets, filters
from rest_framework.response import Response
from .serializers import SampleSerializer,translateSerializer  # APIで渡すデータをJSON,XML変換
from .osaka_rules import translate_text_osaka
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import status
# 大阪弁の翻訳の呼び出し
# 複数の方言を使用する場合、受けとった変数によって切り替える場合urls.pyのurlを要変更

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
    
@api_view(['POST'])
def translate_message(request):
    if request.method == "POST":
        try:
            message_data = request.data.get("message_data", "")
            # 翻訳処理
            translated_data = translate_text_osaka(message_data)  # message_dataを渡す
        except Exception as e:
            # 翻訳処理中に何らかのエラーが発生した場合
            return Response({
                'error': 'Translation failed',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # MessagesModel に保存
        try:
            message = MessagesModel(
                message_data=message_data,
                translated_data=translated_data,
                # 他のフィールドもここで設定
            )
            message.save()
        except Exception as e:
            # データベース保存時に何らかのエラーが発生した場合
            return Response({
                'error': 'Failed to save the message',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # シリアライザを使用してJSON形式に変換
        serializer = SampleSerializer(message)

        # クライアントにレスポンスを返す
        return Response(serializer.data)

    else:
        # POSTリクエスト以外の場合
        return Response({'error': 'This endpoint only supports POST requests.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)