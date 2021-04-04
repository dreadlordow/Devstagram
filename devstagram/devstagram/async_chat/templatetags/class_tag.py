from django import template
from django.core.serializers import deserialize

register = template.Library()

@register.filter(name='get_class')
def get_class(value):
    return value.__class__.__name__


@register.filter(name='get_last_msg')
def get_last_msg(chatroom):
    message = chatroom.message_set.last()
    post_send = chatroom.postmessage_set.last()
    if not post_send:
        return 'Message'
    if message.timestamp > post_send.timestamp:
        return 'Message'
    return 'Post'



# @register.filter(name='deserialize')
# def get_serialized(value):
#     new_objects = []
#     for val in value:
#         obj = deserialize('json', val)
#         new_objects.append(obj)
#     return new_objects