"""nojavan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .api import search_api
from .utils import export_excel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path('likedislike/', include(('likedislike.urls', 'likedislike'), namespace='likedislike')),
    path('posts/', include(('post.urls', 'post'), namespace='post')),
    path('track/', include(('usertracker.urls', 'usertracker'), namespace='usertracker')),
    path('', include(('user.urls', 'user'), namespace='user')),
    path('rate/', include(('rate.urls', 'rate'), namespace='rate')),
    path('message/', include(('message.urls', 'message'), namespace='message')),
    path('api/search/', search_api, name='search_api'),
    path('export/<model>/', export_excel, name='export_excel'),
    path('export/<model>/<action>/', export_excel, name='export_excel'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)