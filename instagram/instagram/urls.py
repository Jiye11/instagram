"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import insta.views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', insta.views.home, name='home'),
    path('sett', insta.views.sett, name='sett'),
    path('', insta.views.loginn, name='loginn'),
    path('create', insta.views.create, name='create'),
    path('update/<int:pk>', insta.views.update, name='update'),
    path('delete/<int:pk>', insta.views.delete, name='delete'),
    path('signin', insta.views.signin, name='signin'),
    path('signup', insta.views.signup, name='signup'),
    path('comment/<int:post_id>', insta.views.comment, name='comment'),
    path('hashtag/<str:hashtag_name>', insta.views.hashtag, name='hashtag'),
    # path('location/<str:location_place>', insta.views.location, name='location'),
    path('like/<int:pk>', insta.views.like, name='like'),
    path('profile', insta.views.profile, name='profile'),
    path('mypage', insta.views.mypage, name='mypage'),

    path('', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
