from django.urls import path
from comment.views import *

urlpatterns = [
    path('send/comment', send_comment, name='send_comment'),
    path('delete/comment', delete_comment, name='delete_comment'),
    path('approve/comment', approve_comment, name='approve_comment'),
]
