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
class Location(models.Model):
    country_region_code = models.CharField(_('country_region_code'),
        max_length=10)
    country_region_name = models.CharField(_('country_region_name'),
        max_length=30)
    country_region_py = models.CharField(_('country_region_py'),
        max_length=30, null=False, default='', blank=True)
    country_region_pinyin = models.CharField(_('country_region_pinyin'),
        max_length=256, null=False, default='', blank=True)
    state_code = models.CharField(_('state_code'), max_length=10, null=False,
        default='', blank=True)
    state_name = models.CharField(_('state_name'), max_length=30,
        null=False, default='', blank=True)
    state_py = models.CharField(_('state_py'),
        max_length=128, null=False, default='', blank=True)
    state_pinyin = models.CharField(_('state_pinyin'),
        max_length=256, null=False, default='', blank=True)
    city_code = models.CharField(_('city_code'), max_length=10, null=False,
        default='', blank=True)
    city_name = models.CharField(_('city_name'), max_length=30,
        null=False, default='', blank=True)
    city_py = models.CharField(_('city_py'),
        max_length=128, null=False, default='', blank=True)
    city_pinyin = models.CharField(_('city_pinyin'),
        max_length=256, null=False, default='', blank=True)
    region_code = models.CharField(_('region_code'),
        max_length=10, null=False, default='', blank=True)
    region_name = models.CharField(_('region_name'),
        max_length=30, null=False, default='', blank=True)
    region_py= models.CharField(_('region_py'),
        max_length=128, null=False, default='', blank=True)
    region_pinyin= models.CharField(_('region_pinyin'),
        max_length=256, null=False, default='', blank=True)
    longitude = models.FloatField(_('longitude'),
        null=False, default=0.0, blank=True)
    latitude = models.FloatField(_('latitude'),
        null=False, default=0.0, blank=True)
    detail_location = models.CharField(_('detail_location'),
        max_length=256, null=False, default='', blank=True)
    is_active = models.BooleanField(_('is_active'), default=False)

    def save(self, *args, **kwargs):
        self.country_region_pinyin = ''.join(lazy_pinyin(self.country_region_name))
        self.country_region_py = ''.join(lazy_pinyin(self.country_region_name, style=Style.FIRST_LETTER))
        self.state_pinyin = ''.join(lazy_pinyin(self.state_name))
        self.state_py = ''.join(lazy_pinyin(self.state_name, style=Style.FIRST_LETTER))
        self.city_pinyin = ''.join(lazy_pinyin(self.city_name))
        self.city_py = ''.join(lazy_pinyin(self.city_name, style=Style.FIRST_LETTER))
        self.region_pinyin = ''.join(lazy_pinyin(self.region_name))
        self.region_py = ''.join(lazy_pinyin(self.region_name, style=Style.FIRST_LETTER))
        super(Location, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        index_together = [
            'country_region_code',
            'state_code',
            'city_code',
            'region_code']

    def __str__(self):
        return '%s-%s-%s-%s' % (self.country_region_name, self.state_name,
            self.city_name, self.region_name)


class Address(models.Model):
    location = models.ForeignKey(Location, related_name='addresses',
        on_delete=models.CASCADE, null=True)
    detail = models.TextField(_('detail'), blank=True,
                                  null=False, default='')
    is_active = models.BooleanField(_('is_active'), default=False)


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
    department = models.ForeignKey('Department', related_name='users',
        on_delete=models.CASCADE, blank=True, null=True)
    rank = models.IntegerField(default=0)
    birthday = models.DateTimeField(blank=True, null=True)
    home_address = models.ForeignKey(Address, related_name='liver',
        on_delete=models.CASCADE, blank=True, null=True)
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

    def __str__(self):
        return self.username


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
    address = models.ForeignKey(Address, related_name='departments',
        on_delete=models.CASCADE, null=True)
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
