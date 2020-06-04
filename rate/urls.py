from django.urls import path
from .views import *

urlpatterns = [
    path('rate/<int:post_id>/', rate_view, name='rate_view'),
]
