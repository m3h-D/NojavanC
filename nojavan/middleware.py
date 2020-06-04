from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django_user_agents.utils import get_user_agent
from django.contrib.sites.shortcuts import get_current_site
from usertracker.models import UserTracker
from nojavan.utils import get_client_ip
from urllib.parse import urlsplit
from django.contrib.auth import get_user_model
import re
from django.urls import resolve

User = get_user_model()

class UserTrackerMiddleware:
    """this middleware track users actions at every link except admin panel
       and when admin goes to ghost mode
       to assign instance to UserTracker will resolve url and then get kwargs of function for that url
       then split the key in the first index there is the model of object for content type and for the id of object
       will use value of the kwargs.
    """    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/admin/' not in request.path and not 'iam_ghosting' in request.session:
            match = resolve(str(request.path))
            instance = None
            try:
                if '_' in str(match.kwargs.keys()):
                    myfilter = {}
                    for key, val in list(match.kwargs.items())[:1]:
                        key_val = str(key).split('_')
                        myfilter[f'{key_val[1]}'] = val
                        model_qs = ContentType.objects.get(model=str(key_val[0]))
                        Model = model_qs.model_class()
                        instance = Model.objects.get(**myfilter)
            except Exception as e:
                # print(str(e))
                pass
                        
            # -----------------------------------------------------
            protocol = urlsplit(request.build_absolute_uri(None)).scheme
            current_site = get_current_site(request)
            current_path = request.path
            url = ''.join(
                [str(protocol), '://', str(current_site), str(current_path)])
            # -----------------------------------------------------
            if request.user.is_authenticated:
                UserTracker.objects.create_by_model(
                    user=request.user,
                    url=url,
                    instance=instance,
                    user_agent=str(get_user_agent(request)),
                    ip_address=get_client_ip(request)
                )
            else:
                try:
                    th_user = get_object_or_404(User, phone=request.session['phone'])
                except:
                    th_user = None
                UserTracker.objects.create_by_model(
                    user=th_user,
                    url=url,
                    instance=instance,
                    user_agent=str(get_user_agent(request)),
                    ip_address=get_client_ip(request)
                )
        response = self.get_response(request)
        return response
