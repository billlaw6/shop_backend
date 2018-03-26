#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# File Name: ".expand("%"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Fri Jan  5 17:32:15 CST 2018
#
# @desc: Social OAuth2采用django-rest-framework-social-oauth2，此包依赖python-social-auth
# 和django-oauth-toolkit两包，django-oauth-toolkit依赖OAuthLib包，python-social-auth参考了
# django-social-auth并替代了它。
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
    email = models.EmailField(_('email address'), null=True, blank=True)
    cell_phone = models.CharField(_('Cell phone'), max_length=20, null=True,
                                  blank=True)
    expired_on = models.DateTimeField(_('Expired on'), default='2070-01-01')
    # avatar = models.ImageField(_('User avatar'), upload_to='user_avatar',
    #                            width_field='width', height_field='height',
    #                            blank=True, null=True)
    width = models.PositiveSmallIntegerField(default=20, blank=True)
    height = models.PositiveSmallIntegerField(default=20, blank=True)

    EMAIL_FIELD = 'email'
    # 决定UserModel._default_manager.get_by_natural_key()取哪个字段
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('Shop user')
        verbose_name_plural = _('Shop users')
