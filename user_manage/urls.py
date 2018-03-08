from django.conf.urls import url

from user_manage import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^logged_out$', views.logged_out, name='logged_out'),
    url(r'^weixin_check', views.weixin_token_check, name='weixin_check'),
]
