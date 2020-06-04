from django.urls import path
from.views import *

urlpatterns = [
    path('chatroom/<int:chatroom_id>/',chat_room, name='chat_room'),
    # path('send-message/<int:user_id>/', send_message, name='send_message'),
    path('send-message/<receivers>/<content>/<room_ids>/', send_message, name='send_message'),
    path('send-message/<int:room_ids>/',send_message, name='send_message'),
    path('message-box/',message_box, name='message_box'),
]