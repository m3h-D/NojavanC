from django.urls import path
from.views import add_to_dislike, add_to_like

urlpatterns = [
    path('like/', add_to_like, name='add_to_like'),
    path('dislike/',add_to_dislike, name='add_to_dislike'),
]