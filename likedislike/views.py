from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.contenttypes.models import ContentType

# Create your views here.
from .models import LikeDislike
import logging

logger = logging.getLogger(__name__)


def add_to_like(request):
    """Like kardane model ha barassase model_type ke to template
    be soorate str pass dade shude.
    """
    if request.is_ajax():
        model_id = request.POST.get('model_id')
        model_type = request.POST.get('model_type')
        content_type = ContentType.objects.get(model=model_type)
        ModelType = content_type.model_class()
        model_type_qs = get_object_or_404(ModelType, id=model_id)
        obj = LikeDislike.objects.create_for_instance_model(
            instance=model_type_qs, request=request, likedislike='like')
        logger.info(f"{model_type_qs} {obj.likedislike}")
        return JsonResponse({"response": f"شما {model_type_qs.title} را پسندیدید"}, status=200)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def add_to_dislike(request):
    """Dislike kardane model ha barassase model_type ke to template
    be soorate str pass dade shude.
    """
    if request.is_ajax():
        model_id = request.POST.get('model_id')
        model_type = request.POST.get('model_type')
        content_type = ContentType.objects.get(model=model_type)
        ModelType = content_type.model_class()
        model_type_qs = get_object_or_404(ModelType, id=model_id)
        obj = LikeDislike.objects.create_for_instance_model(
            instance=model_type_qs, request=request, likedislike='dislike')
        logger.info(f"{model_type_qs} {obj.likedislike}")

        return JsonResponse({"response": f"شما {model_type_qs.title} را نپسندیدید"}, status=200)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))