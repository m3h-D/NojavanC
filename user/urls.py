from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.conf import settings
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('register/', register_view, name='register_view'),
    path('verify/', verification_view, name='verification_view'),
    path('resend/sms/', send_sms_again, name='send_sms_again'),
    path('forget-password/', forget_password, name='forget_password'),
    url(r'^new-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', new_password, name='new_password'),
    
    path('delete/', delete_user, name='delete_user'),
    path('create/', create_user, name='create_user'),
    path('edit-profile/', edit_user, name='edit_user'),
    path('accept-owner/', accept_owner, name='accept_owner'),
    path('edit-profile/<user_username>/', edit_user, name='edit_user'),
    path('list-user/', list_user, name='list_user'),
    path('follow/', follow_user, name='follow_user'),
    path('action/', user_action, name='user_action'),

    path('create-group/', create_group, name='create_group'),
    path('add-group/', add_to_group, name='add_to_group'),
    path('group/<group_slug>/', group_detail, name='group_detail'),
    path('<user_username>/', profile_view, name='profile_view'),
    
]
