from django import template
from django.core.serializers import deserialize

from devstagram.mainsite.models import Friendship

register = template.Library()

@register.filter(name='get_class')
def get_class(value):
    return value.__class__.__name__

# @register.filter(name='deserialize')
# def get_serialized(value):
#     new_objects = []
#     for val in value:
#         obj = deserialize('json', val)
#         new_objects.append(obj)
#     return new_objects