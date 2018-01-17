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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


# Create your models here.
class MyUser(AbstractUser):
    """
    验证方式不一样，所以必须自定义用户模型
    """
    cell_phone = models.CharField(_('Cell phone'), max_length=20, default='')
    weixin = models.CharField(_('weixin'), max_length=50, default='')
    sina = models.CharField(_('sina'), max_length=50, default='')
    expired_on = models.DateTimeField(_('Expired on'), default='1970-01-01')
    avatar = models.ImageField(_('User avatar'), upload_to='user_avatar',
                               width_field='width', height_field='height',
                               null=True)
    width = models.PositiveSmallIntegerField(default=20, blank=True)
    height = models.PositiveSmallIntegerField(default=20, blank=True)
