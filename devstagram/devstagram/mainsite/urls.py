from django.urls import path

from devstagram.mainsite.views import IndexView, PictureUploadView, LikePicture, ProfileView, \
    FriendRequestView, CreateFriendship, PictureDisplayView, PictureEditView, CommentPictureView, \
    ProfilePictureUploadView, SearchView

urlpatterns = [
    path('', IndexView.as_view(), name='landing page'),
    path('index/', IndexView.as_view(), name='index'),
    path('uploadpicture/', PictureUploadView.as_view(), name='upload'),
    path('like/<int:pk>', LikePicture.as_view(), name='like'),
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile'),
    path('friendrequest/', FriendRequestView.as_view(), name='friend request'),
    path('friendship/', CreateFriendship.as_view(), name='friendship'),
    path('profile/<str:slug>/<int:pk>/', PictureDisplayView.as_view(), name='picture display'),
    path('edit/<int:pk>/', PictureEditView.as_view(), name='edit'),
    path('comment/', CommentPictureView.as_view(), name='comment'),
    path('uploadpfp/', ProfilePictureUploadView.as_view(), name='upload pfp'),
    path('search/', SearchView.as_view(), name='search'),

]