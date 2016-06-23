from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^blog/$', BlogEntry.as_view(), name='blog'),
    url(r'^blog/(?P<blog_id>\d+)/$', BlogEntry.as_view(), name='blog_by_id'),
    url(r'^blogs/$', BlogCollection.as_view(), name='blog_list'),
    url(r'^blogs/(?P<page_number>\d+)/$', BlogCollection.as_view(), name='blog_list'),
    url(r'^blog/paragraph/(?P<paragraph_id>\d+)/comment/$', BlogComment.as_view(), name='paragraph_comment')
]
