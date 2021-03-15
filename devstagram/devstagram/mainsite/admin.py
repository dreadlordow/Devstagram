from django.contrib import admin

from devstagram.mainsite.models import *

admin.site.register(Picture)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(ProfilePicture)