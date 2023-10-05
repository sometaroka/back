from django.contrib import admin

# Register your models here.
from .models import PrefecturesModel,EventsModel,DialectsModel,Users,FavoritesModels,TimelinesModel,CommentsModel,LikesModel,FollowsModel,TalksModel,MessagesModel

admin.site.register(PrefecturesModel)
admin.site.register(EventsModel)
admin.site.register(DialectsModel)
admin.site.register(Users)
admin.site.register(FavoritesModels)
admin.site.register(TimelinesModel)
admin.site.register(CommentsModel)
admin.site.register(LikesModel)
admin.site.register(FollowsModel)
admin.site.register(TalksModel)
admin.site.register(MessagesModel)