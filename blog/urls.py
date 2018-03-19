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
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^subscriptions/$', views.subscriptions, name='subscriptions'),
    #url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    #url(r'^post/new/$', views.post_new, name='post_new'),
    #url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^accounts/login/$', authViews.login, name='login'),
    url(r'^accounts/logout/$', authViews.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^accounts/profile/$', views.blog, name='blog'),
    ]
