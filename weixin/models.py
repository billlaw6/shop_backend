#!/usr/bin/env python
#-*-coding=utf-8-*-
#
#File Name: ".expand("%"))
#Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
#Author LiuBin on: Wed Mar 28 09:50:22 CST 2018
#
#@desc:
#
#@history
#

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class APIAccessToken(models.Model):
    """
    存储获取的API access_token
    """
    appid = models.CharField(_('appid'), max_length=128)
    access_token = models.CharField(_('Access Token'), max_length=512)
    expires_in = models.PositiveIntegerField(_('expires_in'))
    created_at = models.DateTimeField(_('created_at'), auto_now=True)
