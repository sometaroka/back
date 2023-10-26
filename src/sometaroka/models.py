from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class UsersModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=128)


class RoomsModel(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user1 = models.ForeignKey(UsersModel, on_delete=models.CASCADE, related_name='rooms_as_user1')
    user2 = models.ForeignKey(UsersModel, on_delete=models.CASCADE, related_name='rooms_as_user2')

class MessagesModel(models.Model):
    msg_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    msg_data = models.CharField(max_length=100)
    msg_date = models.DateTimeField(auto_now_add=True)
    room_id = models.ForeignKey(RoomsModel, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(UsersModel, on_delete=models.CASCADE,null=True)


class Users(AbstractUser):
    #オンライン状態
    profile_introduction = models.CharField(max_length=255, default='ここにデフォルトの自己紹介')





# #都道府県テーブル
# class PrefecturesModel(models.Model):
#     #都道府県ID
#     prefectures_id = models.SmallIntegerField(primary_key=True,)
#     #都道府県名
#     prefectures_name = models.CharField(max_length=10)

# #イベントテーブル
# class EventsModel(models.Model):
#     #イベント情報ID
#     event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     #イベント情報
#     event_info = models.CharField(max_length=400)
#     #都道府県ID
#     prefectures_id = models.ForeignKey(PrefecturesModel,on_delete=models.CASCADE,null=True)

# #方言テーブル
# class DialectsModel(models.Model):
#     #方言ID
#     dialect_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     #方言名
#     dialect_name = models.CharField(max_length=50)
    
# #ユーザーテーブル
# class Users(AbstractUser):
#     #ユーザーネーム
#     #username = models.CharField(max_length=30,unique=True)
#     #パスワード
#     #password = models.CharField(max_length=16)
#     #テーブル設計ではバーキャラだけど修正した
#     #メールアドレス
#     #email = models.EmailField(max_length=319)
#     #プロフィールの自己紹介文
#     profile_introduction = models.CharField(max_length=300)
#     #出身地
#     birth_place = models.CharField(max_length=10)
    
#     # オンライン状態
#     statement = models.BooleanField(default=True)
#     #生年月日
#     date_of_birth = models.CharField(max_length=10)
#     #プロフィールのヘッダー画像
#     profile_header_image = models.CharField(max_length=100)
#     #プロフィールのアイコン画像
#     profile_icon_image = models.CharField(max_length=100)
#     #方言ID
#     dialect_id = models.ForeignKey(DialectsModel,on_delete=models.CASCADE,null=True)

# #お気に入り方言テーブル
# class FavoritesModels(models.Model):
#     #お気に入り方言ID
#     favorite_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     #方言ID
#     dialect_id = models.ForeignKey(DialectsModel,on_delete=models.CASCADE,null=True)
#     #ユーザーID
#     user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)

# #タイムラインテーブル
# class TimelinesModel(models.Model):
#     #投稿ID
#     post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     #投稿画像
#     post_image = models.CharField(max_length=100)
#     #投稿ボイス
#     post_voice = models.CharField(max_length=100)
#     #投稿動画
#     post_movie = models.CharField(max_length=100)
#     #いいね
#     good = models.IntegerField()
#     #投稿日時
#     post_date = models.DateTimeField(auto_now_add=True)
#     #ユーザーID
#     user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)

# #コメントテーブル
# class CommentsModel(models.Model):
#     #コメントID
#     comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     #コメントデータ
#     comment = models.CharField(max_length=100)
#     #投稿ID
#     post = models.ForeignKey(TimelinesModel,on_delete=models.CASCADE,null=True)
#     #ユーザーID
#     user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)

# #いいねテーブル
# class LikesModel(models.Model):
#     #いいね数
#     like_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     #ユーザーID
#     user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)

# #フォロー/フォロワーテーブル
# class FollowsModel(models.Model):
#     #フォローID
#     follow_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     #ユーザーID
#     user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)
#     #ユーザーID（2ついる？ミス？）
#     user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)

# #トークテーブル
# class TalksModel(models.Model):
#     #トークID
#     talk_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

# #メッセージテーブル
# class MessagesModel(models.Model):
#     #メッセージID
#     message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     #メッセージデータ
#     message_data = models.CharField(max_length=100)
#     #メッセージ送信日時
#     massege_date = models.DateTimeField(auto_now_add=True)
#     #イントネーション
#     intnation = models.CharField(max_length=200)
#     #ユーザーID
#     user = models.ForeignKey(Users,on_delete=models.CASCADE,null=True)
#     #トークID
#     talk_id = models.ForeignKey(TalksModel,on_delete=models.CASCADE,null=True)

