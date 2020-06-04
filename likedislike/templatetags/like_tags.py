from django import template
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from likedislike.models import LikeDislike
from nojavan.utils import get_client_ip


register = template.Library()


@register.simple_tag(takes_context=True)
def like_btn_color(context, id, model_type):
    request = context['request']
    ip_address = get_client_ip(request)
    content_type = ContentType.objects.get(model=model_type)
    Model = content_type.model_class()
    model_qs = get_object_or_404(Model, id=id)
    likedislike = LikeDislike.objects.filter_by_model(
        model_qs).filter(likedislike='like').first()
    try:
        if request.user.is_authenticated:
            if likedislike.user == request.user or likedislike.ip_address == ip_address:
                return True
        elif request.user.is_anonymous:
            if likedislike.ip_address == ip_address:
                return True
    except:
        return False


@register.simple_tag(takes_context=True)
def dislike_btn_color(context, id, model_type):
    request = context['request']
    ip_address = get_client_ip(request)
    content_type = ContentType.objects.get(model=model_type)
    Model = content_type.model_class()
    model_qs = get_object_or_404(Model, id=id)
    likedislike = LikeDislike.objects.filter_by_model(
        model_qs).filter(likedislike='dislike').first()
    try:
        if request.user.is_authenticated:
            if likedislike.user == request.user or likedislike.ip_address == ip_address:
                return True
        elif request.user.is_anonymous:
            if likedislike.ip_address == ip_address:
                return True
    except:
        return False


@register.simple_tag
def like_counter(id, model_type):
    content_type = ContentType.objects.get(model=model_type)
    like = LikeDislike.objects.filter(
        content_type=content_type, object_id=id).filter(likedislike='like')
    return like.count()


@register.simple_tag
def dislike_counter(id, model_type):
    content_type = ContentType.objects.get(model=model_type)
    like = LikeDislike.objects.filter(
        content_type=content_type, object_id=id).filter(likedislike='dislike')
    return like.count()