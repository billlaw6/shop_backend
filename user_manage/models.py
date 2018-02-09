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
from social_django.models import UserSocialAuth


# Create your models here.
class ShopUser(AbstractUser):
    """
    验证方式不一样，所以必须自定义用户模型
    """
    email = models.EmailField(_('email address'), unique=True)
    cell_phone = models.CharField(_('Cell phone'), max_length=20, null=True,
                                  unique=True, blank=True)
    expired_on = models.DateTimeField(_('Expired on'), default='2070-01-01')
    # avatar = models.ImageField(_('User avatar'), upload_to='user_avatar',
    #                            width_field='width', height_field='height',
    #                            blank=True, null=True)
    width = models.PositiveSmallIntegerField(default=20, blank=True)
    height = models.PositiveSmallIntegerField(default=20, blank=True)

    EMAIL_FIELD = 'email'
    # 决定UserModel._default_manager.get_by_natural_key()取哪个字段
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('Shop user')
        verbose_name_plural = _('Shop users')
