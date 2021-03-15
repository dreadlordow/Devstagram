from django import forms

from devstagram.chat.models import ChatRoom


class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        exclude = ('user_one', 'user_two', 'last_msg_time')
