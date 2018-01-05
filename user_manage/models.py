#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# File Name: ".expand("%"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Fri Jan  5 17:32:15 CST 2018
#
# @desc:
#
# @history
#

from  django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


# Create your models here.
class MyUser(models.Model):
    """
    在django-user-management的基础上自定义User
    https://github.com/incuna/django-user-management/blob/master/docs/installation.md
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cell_phone = models.CharField(_('Cell phone'), max_length=20, default='')
    weixin = models.CharField(_('weixin'), max_length=50, default='')
    sina = models.CharField(_('sina'), max_length=50, default='')
    expired_on = models.DateTimeField(_('Expired on'), default='')
    avatar = models.ImageField(_('User avatar'), upload_to='user_avatar',
                               width_field='width', height_field='height',
                               null=True)
    width = models.PositiveSmallIntegerField(default=20, blank=True)
    height = models.PositiveSmallIntegerField(default=20, blank=True)
