from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from devstagram.async_chat.models import Message
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

MyModel = Message


@receiver(post_save, sender=MyModel)
def create_notifications(sender, instance, created, *args, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'gossip', {
                'type': 'message.gossip',
                'event': 'New Message',
                'username': instance.receiver.username
            }
        )
        print('crewated')