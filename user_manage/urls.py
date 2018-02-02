from django.conf.urls import url

from user_manage import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^weixin_check', views.weixin_token_check, name='weixin_check'),
    # url(r'^weixin_login', views.WeixinLogin.as_view(), name='weixin_login'),
    url(r'^weixin_login1', views.weixin_login, name='weixin_login1'),
]
