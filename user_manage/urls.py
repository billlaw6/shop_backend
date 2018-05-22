from django.conf.urls import url

from user_manage import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^logged_out$', views.logged_out, name='logged_out'),
    url(r'^weixin_check', views.weixin_token_check, name='weixin_check'),
    url(r'^user_info', views.UserInfo.as_view(), name='user_info'),
    url(r'^user_perms', views.UserPermissions.as_view(), name='user_perms'),
]
