#  APIの出力をJSON,XMLデータに変換
from rest_framework import serializers
from .models import MessagesModel


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagesModel  # 呼び出すモデル
        # fields = ["message_id", "message_data", "massege_date"]  # API上に表示するモデルのデータ項目
        fields = "__all__"  # 指定せず全ての項目をレスポンスする場合

    def create(self, validated_data):
        newMessage = MessagesModel.objects.create(
            message_data=validated_data["message_data"],
            intnation=validated_data["intnation"],
            user=validated_data["user"],
            talk_id=validated_data["talk_id"],
        )
        newMessage.save()
        return newMessage
