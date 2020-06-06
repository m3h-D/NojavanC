from django import template

register = template.Library()

@register.simple_tag
def message_receivers(cahtrooms, user):
    return any(users in user.chatroomreceivers.all() for users in cahtrooms.all())