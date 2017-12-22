#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# File Name: ".expand("%"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Tue Dec 19 16:28:05 CST 2017
#
# @desc:
#
# @history
#
from django.conf.urls import url

from dict_manage import views


urlpatterns = [
    url('^category$', views.category),
]
