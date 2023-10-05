from django.db import models

# Create your models here.


#ここから記述しました。もうちょっと余裕もって依頼して欲しかったな。朝にバイトあるし、明日イベント運営しなきゃいけないんだよ？
#正直私って結構忙しい部類の人間だと思うんだ、そんな私にばっか何でもかんでもやってもらいすぎだともうし、こんな構造になっているのは
#絶対おかしいと思うんだよ。いかがでしょうか
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid



class PrefecturesModel(models.Model):
    prefectures_id = models.SmallIntegerField(primary_key=True,)
    prefectures_name = models.CharField(max_length=10)

class EventsModel(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_info = models.CharField(max_length=400)
    prefectures_id = models.ForeignKey(PrefecturesModel,on_delete=models.CASCADE,null=True)


class DialectsModel(models.Model):
    dialect_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dialect_name = models.CharField(max_length=50)

class Users(AbstractUser):
    #username = models.CharField(max_length=30,unique=True)
    #password = models.CharField(max_length=16)
    #テーブル設計ではバーキャラだけど修正した
    #email = models.EmailField(max_length=319)
    profile_introduction = models.CharField(max_length=300)
    birth_place = models.CharField(max_length=10)
    # ↓何これ
    statement = models.BooleanField(default=True)
    date_of_birth = models.CharField(max_length=10)
    profile_header_image = models.CharField(max_length=100)
    profile_icon_image = models.CharField(max_length=100)
    dialect_id = models.ForeignKey(DialectsModel,on_delete=models.CASCADE,null=True)

class FavoritesModels(models.Model):
    favorite_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dialect_id = models.ForeignKey(DialectsModel,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)

class TimelinesModel(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_image = models.CharField(max_length=100)
    post_voice = models.CharField(max_length=100)
    post_movie = models.CharField(max_length=100)
    good = models.IntegerField()
    post_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)

class CommentsModel(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.CharField(max_length=100)
    post = models.ForeignKey(TimelinesModel,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)

class LikesModel(models.Model):
    like_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)

class FollowsModel(models.Model):
    follow_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)

class TalksModel(models.Model):
    talk_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class MessagesModel(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_data = models.CharField(max_length=100)
    massege_date = models.DateTimeField(auto_now_add=True)
    intnation = models.CharField(max_length=200)
    user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)
    talk_id = models.ForeignKey(TalksModel,on_delete=models.CASCADE,null=True)

