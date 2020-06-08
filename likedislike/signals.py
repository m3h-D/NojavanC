from django.dispatch import Signal

like_signal = Signal(['sender','ip_address','likedislike', 'request'])

def like_dislike_receiver(sender, ip_address, likedislike, request, *args, **kwargs):
    if sender.likedislike == 'like' and likedislike == 'like':
        sender.delete()
    elif sender.likedislike == 'dislike' and likedislike == 'dislike':
        sender.delete()
    elif sender.likedislike == 'like' and likedislike == 'dislike':
        sender.likedislike = 'dislike'
        # if request.user.is_authenticated:
        #     sender.ip_address = ip_address
        #     sender.user = request.user
        sender.save()
    elif sender.likedislike == 'dislike' and likedislike == 'like':
        sender.likedislike = 'like'
        # if request.user.is_authenticated:
        #     sender.ip_address = ip_address
        #     sender.user = request.user
        sender.save()
    return sender

like_signal.connect(like_dislike_receiver)