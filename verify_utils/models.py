#!/usr/bin/env python
#-*-coding=utf-8-*-
#
#File Name: ".expand("%"))
#Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
#Author LiuBin on: Sun Mar 11 18:44:23 CST 2018
#
#@desc:
#
#@history
#


from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class CaptchaRecord(models.Model):
    """
    记录生成过的校验码，用于验证接收到的请求里包含的验证码是否有效，防止机器人攻击。
    """
    client_ip = models.GenericIPAddressField(_('IP address'), protocol='both', unpack_ipv4=False)
    captcha = models.CharField(_('Captcha'), max_length=20)

    encrypted_captcha = models.CharField(_('Encrypted captcha'), max_length=50)
    created_at = models.DateTimeField(_('Created at'), default=timezone.now, db_index=True)

    class Meta:
        verbose_name = _('Captcha record')
        verbose_name_plural = _('Captcha records')


class VerifyCodeRecord(models.Model):
    """
    记录生成过的短信验证码，用于验证接收到的请求里包含的短信验证码是否有效，防止机器人攻击。
    """
    cell_phone = models.CharField(_('Cell phone'), max_length=20)
    verify_code = models.CharField(_('Verify code'), max_length=20)
    verify_content = models.CharField(_('Verify content'), max_length=200)
    created_at = models.DateTimeField(_('Created at'), default=timezone.now, db_index=True)

    class Meta:
        verbose_name = _('Verify code record')
        verbose_name_plural = _('Verify code records')
