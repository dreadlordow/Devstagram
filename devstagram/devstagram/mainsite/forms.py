from django import forms
from django.core.exceptions import ValidationError

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

    # def clean_comment(self):
    #     comment = self.cleaned_data['comment']
    #     print(comment)
    #     if len(comment) < 5:
    #         raise ValidationError('Comment must be at least 5 characters long')
    #     return comment


class ProfilePictureUploadForm(forms.ModelForm):
    class Meta:
        model = ProfilePicture
        fields = ['image']


class SortingForm(forms.Form):
    CHOICES = (
        ('Date Joined', 'date joined'),
        ('Likes', 'likes'),
        ('Friends', 'friends')
    )
    sort = forms.ChoiceField(choices=CHOICES)
