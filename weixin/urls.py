#!/usr/bin/env python
#-*-coding=utf-8-*-
#
#File Name: ".expand("%"))
#Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
#Author LiuBin on: Tue Mar 27 20:30:25 CST 2018
#
#@desc:
#
#@history


from django.conf.urls import url
# from django.urls import path

from weixin import views


app_name = 'weixin'
urlpatterns = [
    # ex: /weixin/
    url(r'^$', views.WeChatAutoReply.as_view(), name='we_chat'),
    # ex: /weixin/user_list
    url(r'^user_list/$', views.UserList.as_view(), name='user_list'),
    url(r'^user_info/$', views.UserInfo.as_view(), name='user_info'),
    url(r'^batch_user_info/$', views.BatchUserInfo.as_view(), name='batch_user_info'),
]
