from django.urls import path
from .views import *

urlpatterns = [
    path('delete/', delete_post, name='delete_post'),
    path('create/', create_post, name='create_post'),
    path('', posts_list, name='post_list'),
    path('<category_slug>/', posts_list, name='post_list'),
    path('detail/<int:post_id>/<slug>/', post_detail, name='post_detail'),
    path('update/<int:post_id>/<slug>/', update_post, name='update_post'),
]