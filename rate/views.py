from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from .models import *
from post.models import Post
from django.contrib import messages
from .forms import *
import logging

logger = logging.getLogger(__name__)
# Create your views here.



def rate_view(request, post_id):
    if request.is_ajax():
        # post_id = request.POST.get('post_id')
        # rate_num = request.POST.get('rate_number')
        post = get_object_or_404(Post, pk=post_id)
        try:
            instance = Rate.objects.get(user=request.user, post=post)
        except:
            instance = None
        rate_form = RateForm(request.POST or None, user=request.user, post=post, instance=instance)
        if rate_form.is_valid():
            rate_form.save()
        # try:
        #     rate = Rate.objects.get(user=request.user, post=post)
        #     rate.rating = rate_num
        #     rate.save()
        # except:
        #     Rate.objects.create(user=request.user, post=post, rating=rate_num)
        else:
            messages.error(request, str(rate_form.errors), extra_tags='failed_rate_form')
            logger.error(str(rate_form.errors.as_data()))

        response = f"شما به پست {post.title} امتیاز {rate_form.instance.rating} را دادید"
        return JsonResponse({'response': response})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))