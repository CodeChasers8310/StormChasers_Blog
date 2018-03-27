from django.conf.urls import url
from . import views
from django.contrib.auth import views as authViews

# Commented urls use old django girls post object
urlpatterns = [
    url(r'^$', views.home, name='post_list'),
    url(r'^home/$', views.home, name='home'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^locations/$', views.locations, name='locations'),
    url(r'^blog/$', views.blog, name='blog'),
    # url(r'^blog_search/(?P<formTags>\d+)/$', views.blog_search, name='blog_search'),
    url(r'^blog_search/(?P<formTags>\w+)/$', views.blog_search, name='blog_search'),
    # (?P<author>\w+)
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^subscriptions/$', views.subscriptions, name='subscriptions'),
    url(r'^post/(?P<post_id>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.new_top_post, name='new_post'),
    url(r'^accounts/login/$', authViews.login, name='login'),
    url(r'^accounts/logout/$', authViews.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^post/(?P<post_id>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^accounts/profile/$', views.my_profile, name='my_profile'),
    # url(r'^delete-image/$', views.delete_image, name='delete-image'),
    url(r'^delete-image/(?P<id>\d+)/$', views.delete_image, name='delete_image'),
    url(r'^post_deleted/$', views.post_deleted, name='post_deleted_after'),
    url(r'^post_deleted/(?P<id>\d+)/$', views.post_deleted, name='post_deleted'),
    # url(r'^new_post/$', views.image_upload, name='new_post'),
    # url(r'^post/new/(?P<post_id>\d+)/$', views.blog, name='blog'),
    # url(r'^post/new/blog/$', views.blog, name='blog'),
    # url(r'^post/new/blog/blog.html', views.blog, name='blog'),
    url(r'^register/$', views.register, name='register'),
    url(r'^pwd_recover/$', views.pwd_recover, name='pwd_recover'),
]
