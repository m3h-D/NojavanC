# from django import template
# from .models import ChatRoom

# register = template.Library()



# @register.simple_tag()
# def room_receivers(room_id):
#     receivers = []
#     try:
#         room = ChatRoom.objects.get(id=room_id)
#         for user in room.receivers.all():
#             receivers.append(user.id)
#     finally:
#         return receivers
