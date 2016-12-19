"""course_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from personal_page import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^(?P<account_id>[0-9]+)/$', views.BlogView.as_view(), name='account'),
    url(r'^(?P<account_id>[0-9]+)/edit_profile/$', views.EditProfile.as_view(), name='edit_profile'),
    url(r'^(?P<account_id>[0-9]+)/posting/$', views.posting, name='posting'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^registration/', include('register.urls')),
    url(r'^(?P<account_id>[0-9]+)/detail_(?P<post_id>[0-9]+)/$', views.CommentsView.as_view(), name='detail'),
    url(r'^(?P<account_id>[0-9]+)/detail_(?P<post_id>[0-9]+)/comment/$', views.comment, name='comment'),
    url(r'^like-blog/$', views.like_count_blog, name='liker'),
    url(r'^add_friend_(?P<account_id>[0-9]+)/$', views.add_friend, name='add_friend'),
    url(r'^remove_friend_(?P<account_id>[0-9]+)/$', views.remove_friend, name='remove_friend'),
    url(r'^search_result/', views.search, name='search'),
    url(r'^(?P<account_id>[0-9]+)/', include('alpha.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
