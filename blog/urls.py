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
    #url(r'^get_forecast/(?P<lat>\w+)(?P<lon>\w+)(?P<zip>\w+)/$', views.getForecast, name='get_forecast'),
    url(r'^get_forecast/$', views.getForecast, name='get_forecast'),
    url(r'^blog_search/$', views.blog_search, name='blog_search'),
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
    url(r'^post/(?P<post_id>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<post_id>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<post_id>\d+)/remove/$', views.comment_remove, name='comment_remove'),
# post views
####
    #url(r'^blog/login/$', views.user_login, name='login'),
    # login / logout urls
    #url(r'^login/$','django.contrib.auth.views.login', name='login'),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    #url(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    #url(r'^$', views.my_profile, name='my_profile'),

# change password urls
    url(r'^password-change/$', authViews.password_change, name='password_change'),
    url(r'^password-change/done/$',authViews.password_change_done, name='password_change_done'),
    url(r'^edit/$', views.edit, name='edit'),
]
