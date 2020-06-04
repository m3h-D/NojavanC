from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Avg
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from nojavan.utils import search_engine
from category.models import Category
from .models import Post
from rate.models import Rate
from .forms import *
import logging

logger = logging.getLogger(__name__)
# Create your views here.


def posts_list(request, category_slug=None):
    posts = Post.objects.published()
    searches = request.GET
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)
    if searches:
        posts = search_engine(searches, posts)
    return render(request, 'post/list.html', {"posts": posts})


def post_detail(request, post_id, slug):
    post = get_object_or_404(Post, id=post_id, slug=slug)
    avg_rate = post.rate.get_avg_rate(post)
    return render(request, 'post/detail.html', {"post": post, 'avg_rate': avg_rate})



@staff_member_required
def create_post(request):
    categories = Category.objects.all()
    form = AddPostForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            for cat in request.POST.getlist('category_id'):
                form.instance.category.add(cat)
            return redirect(form.instance.get_absolute_url)
        else:
            messages.error(request, f"{form.errors}", extra_tags='post_create_error')
            logger.error(str(form.errors.as_data()))

    return render(request, 'post/create.html', {'form': form, 'categories': categories})



@staff_member_required
def update_post(request, post_id, slug):
    post = get_object_or_404(Post, id=post_id, slug=slug)
    categories = Category.objects.all()

    update_form = AddPostForm(data=request.POST or None,
                              files=request.FILES or None,
                              user=request.user,
                              instance=post)
    if request.method == 'POST':
        if update_form.is_valid():
            update_form.instance.category.clear()
            for cat in request.POST.getlist('category_id'):
                update_form.instance.category.add(cat)
            update_form.save()
            return redirect(update_form.instance.get_absolute_url)
        else:
            messages.error(request, f"{update_form.errors}", extra_tags='post_update_error')
            logger.error(str(update_form.errors.as_data()))

    return render(request, 'post/update.html', {'update_form': update_form, 'categories': categories})


@staff_member_required
def delete_post(request):
    if request.is_ajax():
        post_id = request.POST.get('user_id') 
        post = get_object_or_404(Post, id=post_id)
        response = f"پست {post.title} حذف شد"
        post.delete()
        logger.info(f'deleted post: {post.id}-{post.title}')
        return JsonResponse({"response": response})
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))