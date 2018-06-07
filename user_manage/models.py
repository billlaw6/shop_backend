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
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from social_django.models import UserSocialAuth
from pypinyin import lazy_pinyin, Style


# Create your models here.
class ShopUser(AbstractUser):
    """
    验证方式不一样，所以必须自定义用户模型
    """
    email = models.EmailField(_('email address'), null=True, blank=True)
    cell_phone = models.CharField(_('Cell phone'), max_length=20, null=True,
                                  blank=True)
    py_code = models.CharField(max_length=8, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=60, blank=True, null=True)
    department = models.ForeignKey("Department", on_delete=models.CASCADE,
        blank=True, null=True)
    rank = models.IntegerField(default=0)
    birthday = models.DateTimeField(blank=True, null=True)
    home_address = models.CharField(max_length=200, blank=True, null=True)
    home_phone = models.CharField(max_length=20, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    register_on = models.DateTimeField(blank=True, null=True)
    expired_on = models.DateTimeField(_('Expired on'), default='2070-01-01')
    avatar = models.ImageField(_('User avatar'), upload_to='user_avatar',
                               width_field='width', height_field='height',
                               blank=True, null=True)
    width = models.PositiveSmallIntegerField(default=20, blank=True)
    height = models.PositiveSmallIntegerField(default=20, blank=True)

    EMAIL_FIELD = 'email'
    # 决定UserModel._default_manager.get_by_natural_key()取哪个字段
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('Shop user')
        verbose_name_plural = _('Shop users')


class Group(models.Model):
    name = models.CharField(max_length=128)
    pinyin = models.CharField(max_length=50, blank=True, null=False, default='')
    py = models.CharField(max_length=50, blank=True, null=False, default='')
    members = models.ManyToManyField(
        ShopUser,
        through='GroupShopUserRelation',
        through_fields=('group', 'shop_user'),
    )
    created_at = models.DateTimeField(_('created_at'), auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='created_groups')

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(Group, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name


class GroupShopUserRelation(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    shop_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="membership_invites",
    )
    invite_reason = models.CharField(max_length=128)


class Department(models.Model):
    code = models.CharField(unique=True, max_length=5)
    name = models.CharField(unique=True, max_length=64)
    pinyin = models.CharField(max_length=64, blank=True, null=True)
    py = models.CharField(max_length=16, blank=True, null=True)
    # members = models.ManyToManyField(
    #     ShopUser,
    #     through='DepartmentShopUserRelation',
    #     through_fields=('department', 'shop_user'),
    # )
    address = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=13, blank=True, null=True)
    is_active = models.BooleanField(_('is_active'), default=False)
    created_at = models.DateTimeField(_('created_at'), auto_now=True)

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(Department, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name


# class DepartmentShopUserRelation(models.Model):
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     shop_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     comment = models.CharField(max_length=256, blank=True, null=True)


class DictEmployeeRank(models.Model):
    code = models.CharField(unique=True, max_length=5)
    name = models.CharField(unique=True, max_length=64)
    pinyin = models.CharField(max_length=64, blank=True, null=True)
    py = models.CharField(max_length=16, blank=True, null=True)
    comment = models.CharField(max_length=256, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(DictEmployeeRank, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class DictEmployeeStatus(models.Model):
    code = models.CharField(unique=True, max_length=5)
    name = models.CharField(unique=True, max_length=64)
    pinyin = models.CharField(max_length=64, blank=True, null=True)
    py = models.CharField(max_length=16, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(DictEmployeeStatus, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class DictSex(models.Model):
    code = models.CharField(unique=True, max_length=5)
    name = models.CharField(unique=True, max_length=64)
    pinyin = models.CharField(max_length=64, blank=True, null=True)
    py = models.CharField(max_length=16, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(DictSex, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class DictUserStatus(models.Model):
    code = models.CharField(unique=True, max_length=5)
    name = models.CharField(unique=True, max_length=64)
    pinyin = models.CharField(max_length=64, blank=True, null=True)
    py = models.CharField(max_length=16, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(DictUserStatus, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
