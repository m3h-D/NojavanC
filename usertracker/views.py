from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
import os


def all_logs(request):
    """[open mylog.log to show all requsets to site in html, 
        if user is superuser]
    Arguments:
        request {[GET]} -- [show every requests to site]
    Returns:
        [DICT] -- [every logs stored in mylogs.log linear]
    """
    if request.user.is_superuser:
        the_logs = []
        with open(os.path.join(settings.BASE_DIR, 'logs/mylog.log'), 'r', encoding="utf8") as f:
            for line in f:
                the_logs.append(line)
        return render(request, 'logs/logs.html', {'the_logs': the_logs})
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def url_logs(request):
    """[open django_request.log to show all requsets to urls in html, 
        if user is superuser]
    Arguments:
        request {[GET]} -- [show every requests to urls]
    Returns:
        [DICT] -- [every logs stored in django_request.log linear]
    """
    if request.user.is_superuser:
        the_logs = []
        with open(os.path.join(settings.BASE_DIR, 'logs/django_request.log'), 'r', encoding="utf8") as f:
            for line in f:
                the_logs.append(line)
        return render(request, 'logs/logs2.html', {'the_logs': the_logs})
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
