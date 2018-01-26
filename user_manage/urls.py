from django.conf.urls import url

from user_manage import views

urlpatterns = [
    url(r'^weixin_check', views.weixin_token_check, name='weixin'),
]
