from django.urls import path

from devstagram.mainsite.views import IndexView, PictureUploadView, LikePicture, ProfileView, \
    FriendRequestView, CreateFriendship, PictureDisplayView, PictureEditView, CommentPictureView, \
    ProfilePictureUploadView, SearchView, DeleteCommentView, SendPostViaMessage, PictureDeleteView

urlpatterns = [
    # Register/Login page
    path('', IndexView.as_view(), name='landing page'),

    # Home page
    path('index/', IndexView.as_view(), name='index'),

    # Upload new pictures
    path('uploadpicture/', PictureUploadView.as_view(), name='upload'),

    # Like pictures
    path('like/<int:pk>', LikePicture.as_view(), name='like'),

    # View user profiles
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile'),

    # View user pictures
    path('profile/<str:slug>/<int:pk>/', PictureDisplayView.as_view(), name='picture display'),

    # Send friend requests
    path('friendrequest/', FriendRequestView.as_view(), name='friend request'),

    # Create friendships
    path('friendship/', CreateFriendship.as_view(), name='friendship'),

    # Edit photos
    path('edit/<int:pk>/', PictureEditView.as_view(), name='edit'),

    # Delete photos
    path('delete/<int:pk>/', PictureDeleteView.as_view(), name='delete picture'),

    # Comment photos
    path('comment/', CommentPictureView.as_view(), name='comment'),

    # Delete comment
    path('deletecomment/<int:pk>/', DeleteCommentView.as_view(), name='delete comment'),

    # Upload/Change profile picture
    path('uploadpfp/', ProfilePictureUploadView.as_view(), name='upload pfp'),

    # Search for users
    path('search/', SearchView.as_view(), name='search'),

    # Send post via message
    path('sendpost/', SendPostViaMessage.as_view(), name='send post'),
]