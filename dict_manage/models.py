#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# File Name: ".expand("%"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Wed Nov 22 17:13:58 CST 2017
#
# @desc:
#
# @history
#
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from pypinyin import lazy_pinyin, Style
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class Product(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=128)
    pinyin = models.CharField(max_length=64, blank=True, null=False, default='')
    py = models.CharField(max_length=64, blank=True, null=False, default='')
    brand = models.CharField(_('brand'), max_length=64, null=False, default='',
                             blank=True)
    # 这里带一张主图片，减少请求次数或关联查询
    image = models.ImageField(_('image'), upload_to='shop_frontend/dist/static/img',
                              blank=False, null=False)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2,
                                default=0.00)
    sale_price = models.DecimalField(_('sale_price'), max_digits=9,
                                     decimal_places=2, blank=True, default=0.00)
    is_active = models.BooleanField(_('is_active'), default=False)
    pinyin = models.CharField(max_length=50, blank=True, null=False, default='')
    py = models.CharField(max_length=50, blank=True, null=False, default='')
    is_bestseller = models.BooleanField(_('is_bestseller'), default=False)
    description = models.TextField(_('description'), blank=True, null=False,
                                   default='')
    meta_keywords = models.CharField(_('meta keywords'), max_length=256,
                                     help_text=_('Comma-delimited set of \
                                     SEO keywords for meta tag'), blank=True,
                                     null=False, default='')
    meta_description = models.CharField(_('meta description'), max_length=256,
                                        help_text=_('Content for description \
                                        meta tag'), blank=True, null=False,
                                        default='')
    manufacturer = models.CharField(_('manufacturer'), max_length=256,
                                    blank=True, default='')
    created_at = models.DateTimeField(_('created_at'), auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='created_products')
    updated_at = models.DateTimeField(_('updated_at'), auto_now_add=True)
    updated_by = models.ForeignKey(get_user_model(),
                                   related_name='updated_products')
    highlighted = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=128)
    pinyin = models.CharField(max_length=64, blank=True, null=False, default='')
    py = models.CharField(max_length=64, blank=True, null=False, default='')
    is_active = models.BooleanField(_('is_active'), default=False)
    products = models.ManyToManyField(
        Product,
        through='CategoryTag',
        through_fields=('category', 'product')
    )
    description = models.TextField(_('description'), blank=True, null=False,
                                   default='')
    meta_keywords = models.CharField(_('meta keywords'), max_length=256,
                                     help_text=_('Comma-delimited set of \
                                     SEO keywords for meta tag'), blank=True,
                                     null=False, default='')
    meta_description = models.CharField(_('meta description'), max_length=256,
                                        help_text=_('Content for description \
                                        meta tag'), blank=True, null=False,
                                        default='')
    created_at = models.DateTimeField(_('created_at'), auto_now=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='created_categories')
    updated_at = models.DateTimeField(_('updated_at'), auto_now_add=True)
    updated_by = models.ForeignKey(get_user_model(),
                                   related_name='updated_categories')
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name


class CategoryTag(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag_adder = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="Tag_adder"
    )
    tag_reason = models.CharField(max_length=128)


class ProductPicture(models.Model):
    product = models.ForeignKey(Product, related_name=_('pictures'),
                                blank=False, null=False,
                                on_delete=models.CASCADE)
    name = models.CharField(_('name'), unique=True, max_length=128)
    pinyin = models.CharField(max_length=64, blank=True, null=False, default='')
    py = models.CharField(max_length=64, blank=True, null=False, default='')
    image = models.ImageField(_('image'), upload_to='product_photo',
                              blank=False, null=False)
    order = models.PositiveSmallIntegerField(_('order'), null=False, default=1)
    description = models.TextField(
                                   _('description'),
                                   blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(ProductPicture, self).save(*args, **kwargs)

    class Meta:
        ordering = ('product', 'order', )

    def __str__(self):
        return self.product.name + '-' + self.name


class Express(models.Model):
    code = models.CharField(_('code'), unique=True, max_length=128)
    name = models.CharField(_('name'), unique=True, max_length=128)
    pinyin = models.CharField(max_length=64, blank=True, null=False, default='')
    py = models.CharField(max_length=64, blank=True, null=False, default='')
    is_active = models.BooleanField(_('is_active'), default=False)
    description = models.TextField(
        _('description'),
        blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(Express, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name


class Payment(models.Model):
    code = models.CharField(_('code'), unique=True, max_length=128)
    name = models.CharField(_('name'), unique=True, max_length=128)
    pinyin = models.CharField(max_length=64, blank=True, null=False, default='')
    py = models.CharField(max_length=64, blank=True, null=False, default='')
    is_active = models.BooleanField(_('is_active'), default=False)
    description = models.TextField(
                                   _('description'),
                                   blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(Payment, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name


class OrderStatus(models.Model):
    code = models.CharField(_('code'), unique=True, max_length=128)
    name = models.CharField(_('name'), unique=True, max_length=128)
    pinyin = models.CharField(max_length=64, blank=True, null=False, default='')
    py = models.CharField(max_length=64, blank=True, null=False, default='')
    is_active = models.BooleanField(_('is_active'), default=False)
    description = models.TextField(
                                   _('description'),
                                   blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(OrderStatus, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name


class Location(models.Model):
    country_region_code = models.CharField(
        _('country_region_code'), max_length=10)
    country_region_name = models.CharField(
        _('country_region_name'), max_length=30)
    country_region_py_code = models.CharField(
        _('country_region_py_code'),
        max_length=30, null=False, default='', blank=True)
    country_region_quanpin = models.CharField(
        _('country_region_quanpin'),
        max_length=256, null=False, default='', blank=True)
    state_code = models.CharField(
        _('state_code'),
        max_length=10,
        null=False, default='',
        blank=True)
    state_name = models.CharField(
        _('state_name'),
        max_length=30,
        null=False, default='',
        blank=True)
    state_py_code = models.CharField(
        _('state_py_code'),
        max_length=128, null=False, default='', blank=True)
    state_quanpin = models.CharField(
        _('state_quanpin'),
        max_length=256, null=False, default='', blank=True)
    city_code = models.CharField(
        _('city_code'),
        max_length=10,
        null=False, default='',
        blank=True)
    city_name = models.CharField(
        _('city_name'),
        max_length=30,
        null=False, default='',
        blank=True)
    city_py_code = models.CharField(
        _('city_py_code'),
        max_length=128, null=False, default='', blank=True)
    city_quanpin = models.CharField(
        _('city_quanpin'),
        max_length=256, null=False, default='', blank=True)
    region_code = models.CharField(
        _('region_code'),
        max_length=10, null=False, default='', blank=True)
    region_name = models.CharField(
        _('region_name'),
        max_length=30, null=False, default='', blank=True)
    region_py_code = models.CharField(
        _('region_py_code'),
        max_length=128, null=False, default='', blank=True)
    region_quanpin = models.CharField(
        _('region_quanpin'),
        max_length=256, null=False, default='', blank=True)
    longitude = models.FloatField(
        _('longitude'),
        null=False,
        default=0.0,
     blank=True)
    latitude = models.FloatField(
        _('latitude'),
        null=False,
        default=0.0,
     blank=True)
    detail_location = models.CharField(
        _('detail_location'),
        max_length=256, null=False, default='', blank=True)

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        index_together = [
            'country_region_code',
            'state_code',
            'city_code',
            'region_code']

    def __str__(self):
        return self.country_region_name + '|' + self.state_name + '|'\
            + self.city_name + '|' + self.region_name
