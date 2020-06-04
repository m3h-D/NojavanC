from django.urls import path
from .views import *

urlpatterns = [
    path('all/', all_logs, name='all_logs'),
    path('requests/', url_logs, name='url_logs'),
]
