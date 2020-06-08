from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import ChatRoom, Message
from .forms import SendMessageForm
from django.contrib.auth import get_user_model
# from django.db import transaction
import re
import logging

logger = logging.getLogger(__name__)

# Create your views here.
User = get_user_model()


def chat_room(request, chatroom_id):
    room = get_object_or_404(ChatRoom, pk=chatroom_id)
    chats = None
    if request.user in room.receivers.all():
        chats = Message.objects.filter(room=room)
        for message in chats:
            if message.sender == request.user: break
            if message.is_readed == True: continue
            message.is_readed = True
            message.save()
    context = {"chats": chats, "room": room}
    return render(request, 'message/room.html', context)


# @require_POST
def send_message(request, receivers=None, content=None, chatroom_id=None):
    if receivers:
        all_receivers = list(dict.fromkeys(re.findall(r'\d+', receivers)))
        # all_receivers.append(request.user.id)
        print(all_receivers)
        # print(chatroom_id)
        if chatroom_id:
            chatroom_id = (room_id for room_id in re.findall(r'\d+', chatroom_id))
        for i, id in enumerate(all_receivers, 1):
            message_form = SendMessageForm(request.POST, user=request.user, ajax_content=content)
            if message_form.is_valid(): 
                # user = get_object_or_404(User, id=int(id))
                try:
                    room = ChatRoom.objects.get(id=int(chatroom_id.__next__()))
                    # print(room)
                except (ChatRoom.DoesNotExist, Exception):
                    room = ChatRoom.objects.create()
                    room.receivers.add(int(id))
                    room.receivers.add(request.user)
                message_form.instance.room = room
                # message_form.instance.receiver = user
                message_form.save()
                if i >= len(all_receivers): 
                    messages.success(request, 'پیام با موفقیت ارسال شد')
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            else:
                messages.error(request, str(message_form.errors), extra_tags='failed_bulk_message')
                logger.error(str(message_form.errors.as_data()))
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
                # return HttpResponse(message_form.errors)
    else:
        message_form = SendMessageForm(request.POST, user=request.user)
        if message_form.is_valid(): 
            room = get_object_or_404(ChatRoom, id=int(chatroom_id))
            message_form.instance.room = room
            message_form.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, str(message_form.errors), extra_tags='failed__message')
            logger.error(str(message_form.errors.as_data()))
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))



    # all_receivers = list(dict.fromkeys(re.findall(r'\d+', receivers + str(request.user.id))))
    # message_form = SendMessageForm(request.POST, user=request.user, content=content)
    # if message_form.is_valid():
    #     try:
    #         room = ChatRoom.objects.get(id=int(room_id))
    #     except ChatRoom.DoesNotExist:
    #         room = ChatRoom.objects.create()
    #     [room.receivers.add(int(receiver)) for i, receiver in enumerate(all_receivers, 1) if i < len(all_receivers)]
    #     message_form.instance.room = room
    #     message_form.save()
    # else:
    #     messages.error(request, str(message_form.errors), extra_tags='failed_bulk_message')
    #     logger.error(str(message_form.errors.as_data()))





    # with transaction.atomic():
        # if content and group:



    # for i, receiver in enumerate(all_receivers, 1):
    #     while i < len(all_receivers):
    #         room.receivers.add(int(receiver))


def message_box(request):
    all_rooms = ChatRoom.objects.all()
    return render(request, 'message/message-box.html', {"all_rooms": all_rooms})

