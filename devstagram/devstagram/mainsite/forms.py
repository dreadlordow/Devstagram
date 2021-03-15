from django import forms

from devstagram.mainsite.models import Picture, FriendRequest, Friendship, Comment, ProfilePicture


class PictureUploadForm(forms.ModelForm):
    class Meta:
        model = Picture
        exclude = ('user', 'likes')


class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = ['sender', 'receiver']


class FriendshipForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = '__all__'


class PictureUpdateForm(forms.ModelForm):
    picture = forms.ImageField(required=False)

    class Meta:
        model = Picture
        fields = ['picture', 'description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class ProfilePictureUploadForm(forms.ModelForm):
    class Meta:
        model = ProfilePicture
        fields = ['image']
