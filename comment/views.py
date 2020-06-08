from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .models import Comments
from .forms import CommentForm
from post.models import Post

# Create your views here.


def delete_comment(request):
    """function baraye pak kardane comment"""
    
    if request.is_ajax():
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comments, id=comment_id)
        if request.user == comment.user or request.user.is_admin or request.user.is_staff:
            messages.success(request, f"کامنت {comment.content} با موفقیت حذف شد")
            comment.delete()
            return JsonResponse({"success": "success"})
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def approve_comment(request):
    if request.is_ajax():
        comment_id = request.POST.get('comment_id')
        if request.user.is_staff:
            comment = get_object_or_404(Comments, id=comment_id)
            if comment.approved == True:
                comment.approved = False
            else:
                comment.approved = True
            comment.save()
            messages.success(request, "کامنت مورد تایید شما قرار گرفت")
            return JsonResponse({"success": "success"})
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def send_comment(request):
    """valid kardane comment form baraye har Model"""
    """try baraye ine ke motmaen shim data ei ke be parent_id dadan hatman int bashe (security)"""
    if request.is_ajax():
        post_id = int(request.POST.get('post_id'))
        parent_id = int(request.POST.get('parent_id'))

        if parent_id:
            try:
                parent_obj = Comments.objects.filter(
                    id=parent_id).last()
            except:
                parent_obj = None
        comments_form = CommentForm(request.POST or None)
        if comments_form.is_valid():
            comments_form.instance.user = request.user
            comments_form.instance.post = get_object_or_404(Post, pk=post_id)
            comments_form.instance.parent = parent_obj
            comments_form.save()
            return JsonResponse({"success": "success"})
        else:
            messages.error(request, str(comments_form.errors), extra_tags='comment_errors')
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))