from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^messages/$', views.ConversationsView.as_view(), name='conversations'),
    url(r'^messages_(?P<companion_id>[0-9]+)/$', views.messages, name='messages'),
    url(r'^post_(?P<companion_id>[0-9]+)/$', views.Post, name='post'),
    url(r'^messages_box_(?P<companion_id>[0-9]+)/$', views.messages_box, name='messages_box'),
]