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
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from pypinyin import lazy_pinyin, Style
from user_manage.models import Department


class Product(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=128)
    pinyin = models.CharField(max_length=64, blank=True, null=False, default='')
    py = models.CharField(max_length=64, blank=True, null=False, default='')
    brand = models.CharField(_('brand'), max_length=64, null=False, default='',
                             blank=True)
    # 这里带一张主图片，减少请求次数或关联查询
    image = models.ImageField(_('image'), upload_to='shop_frontend/dist/static/img',
                              blank=False, null=False, default='')
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2,
                                default=0.00)
    sale_price = models.DecimalField(_('sale_price'), max_digits=9,
                                     decimal_places=2, blank=True, default=0.00)
    is_active = models.BooleanField(_('is_active'), default=False)
    pinyin = models.CharField(max_length=64, blank=True, null=False, default='')
    py = models.CharField(max_length=64, blank=True, null=False, default='')
    effective_month = models.IntegerField(blank=True, null=True)
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
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='created_products')
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)
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
    products = models.ManyToManyField(Product, through='CategoryProductRelation',
                                    through_fields=('category', 'product'))
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
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class CategoryProductRelation(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    manager = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="manager"
    )
    reason = models.CharField(max_length=128, blank=True, null=True)


class ProductPicture(models.Model):
    product = models.ForeignKey(Product, related_name=_('pictures'),
                                blank=False, null=False,
                                on_delete=models.CASCADE)
    name = models.CharField(_('name'), unique=True, max_length=128)
    pinyin = models.CharField(max_length=64, blank=True, null=False, default='')
    py = models.CharField(max_length=64, blank=True, null=False, default='')
    is_active = models.BooleanField(_('is_active'), default=False)
    image = models.ImageField(_('image'), upload_to='product_photo',
                              blank=False, null=False)
    order = models.PositiveSmallIntegerField(_('order'), null=False, default=1)
    description = models.TextField(
                                   _('description'),
                                   blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

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
    description = models.TextField(_('description'), blank=True, null=False,
                                  default='')
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(Express, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Payment(models.Model):
    code = models.CharField(_('code'), unique=True, max_length=128)
    name = models.CharField(_('name'), unique=True, max_length=128)
    pinyin = models.CharField(max_length=64, blank=True, null=False, default='')
    py = models.CharField(max_length=64, blank=True, null=False, default='')
    is_active = models.BooleanField(_('is_active'), default=False)
    description = models.TextField(_('description'), blank=True,
                                   null=False, default='')
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

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
    description = models.TextField(_('description'),
                                   blank=True, null=False, default='')
    # created_at = models.DateTimeField(_('created_at'), default=timezone.now)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    def save(self, *args, **kwargs):
        self.pinyin = ''.join(lazy_pinyin(self.name))
        self.py = ''.join(lazy_pinyin(self.name, style=Style.FIRST_LETTER))
        super(OrderStatus, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.name


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
        return self.country_region_name + '|' + self.state_name + '|'\
            + self.city_name + '|' + self.region_name


class Address(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='addresses', null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    detail = models.TextField(_('detail'), blank=True,
                                  null=False, default='')
    is_active = models.BooleanField(_('is_active'), default=False)


class Order(models.Model):
    order_no = models.CharField(max_length=64, unique=True, blank=True,
                                default='')
    payment = models.ForeignKey(Payment, related_name=_('orders'),
                                blank=True, null=True)
    buyer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='orders', null=False)
    sum_price = models.DecimalField(_('sum_price'), max_digits=9, decimal_places=2,
                                default=0.00)
    address = models.ForeignKey(Address, related_name=_('order_address'),
                              blank=True, null=True)
    comment = models.CharField(_('comment'), max_length=128, default='')
    status = models.ForeignKey(OrderStatus, related_name=_('orders'),
                               default=1)
    express = models.ForeignKey(Express, related_name=_('orders'),
                                null=True, blank=True)
    express_no = models.CharField(_('express_no'), max_length=128,
                                  blank=True, null=False, default='')
    express_info = models.TextField(_('express_info'),
                                    blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                   related_name='created_orders', null=False)

    class Meta:
        ordering = ('created_at',)
        index_together = ['order_no', 'created_at', 'express_no']
        # unique_together包含的字段不能为空，字段定义里写blank=True也不行
        unique_together = (('buyer', 'comment'))

    def __str__(self):
        return self.order_no + '-' + self.buyer.username+ '-' + str(self.sum_price)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name=_('order'),
                                blank=False, null=False)
    product = models.ForeignKey(Product, related_name=_('order_detail'),
                                blank=False, null=False)
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2,
                                default=0.00)
    comment = models.CharField(_('comment'), max_length=300, blank=True,
                               default='')
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
        index_together = ['order', 'product']
        unique_together = (('order', 'product'))

    def __str__(self):
        return self.order.order_no + '-' + self.product.name


class VisitLog(models.Model):
    from_ip = models.GenericIPAddressField(_('from_ip'))
    visit_url = models.URLField(_('visit_url'))
    visit_date = models.DateTimeField(null=False, default='')
    browser = models.CharField(_('browser'), max_length=64, null=False, default='',
                              blank=True)
    longitude = models.FloatField(_('longitude'), null=False, default=0, blank=True)
    latitude = models.FloatField(_('latitude'), null=False, default=0, blank=True)

    class Meta:
        ordering = ('visit_date', 'from_ip',)
        verbose_name = _('VisitLog')
        verbose_name_plural = _('VisitLogs')

    def __str__(self):
        return self.visit_date + '-' + self.from_ip


class Stock(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                            related_name=_('stock_record'), null=False)
    product = models.ForeignKey(Product, related_name=_('stock_record'),
                                blank=False, null=False)
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    max_amount = models.DecimalField(_('max_amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    min_amount = models.DecimalField(_('min_amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    location = models.CharField(max_length=256, blank=True, null=True)
    comment = models.CharField(max_length=256, blank=True, null=True)
    status = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        ordering = ('department', 'product',)
        index_together = ['department', 'product',]
        unique_together = (('department', 'product',))

    def __str__(self):
        return self.department.name + '-' + self.product.name


class StockMoveRecord(models.Model):
    page_no = models.CharField(max_length=64, unique=True, blank=True,
                                default='')
    moved_on = models.DateTimeField()
    product = models.ForeignKey(Product, related_name=_('stock_move_record'),
                                blank=False, null=False)
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    rest_amount = models.DecimalField(_('rest_amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2,
                                default=0.00)
    entered_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                            related_name='entered_stock_move_records', null=False)
    processed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                            related_name='processed_stock_move_records', null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField(blank=False, null=False, default=0)
    dept_in = models.ForeignKey(Department, on_delete=models.CASCADE,
                             related_name='in_stock_move_records', null=False)
    dept_out = models.ForeignKey(Department, on_delete=models.CASCADE,
                             related_name='out_stock_move_records', null=True)

    class Meta:
        ordering = ('dept_in', 'dept_out', 'status', 'page_no', 'product',)
        index_together = ['page_no', 'dept_in',]
        unique_together = (('page_no', 'dept_in', 'dept_out', 'product',))

    def __str__(self):
        return self.dpet_in.name + '-' + self.page_no + '-' + self.product.name + '-' + self.amount


class StockCheck(models.Model):
    page_no = models.CharField(max_length=64, unique=True, blank=True,
                                default='')
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                             null=False)
    product = models.ForeignKey(Product, related_name=_('stock_check_record'),
                                blank=False, null=False)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2,
                                default=0.00)
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    check_amount = models.DecimalField(_('check_amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    location = models.CharField(max_length=256, blank=True, null=True)
    comment = models.CharField(max_length=256, blank=True, null=True)
    status = models.IntegerField(blank=False, null=False, default=0)
    entered_on = models.DateTimeField(_('entered_on'), auto_now=True)
    entered_by = models.ForeignKey(get_user_model(), related_name=_('entered_stock_check_records'),
        on_delete=models.CASCADE, null=False)
    checked_on = models.DateTimeField(_('checked_on'), blank=True, null=True)
    checked_by = models.ForeignKey(get_user_model(), related_name=_('checked_stock_check_records'),
        on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('department', 'page_no', 'product', 'status', )
        index_together = ['page_no', 'department',]
        unique_together = (('page_no', 'department', 'product',))

    def __str__(self):
        return self.department.name + '-' + self.page_no + '-' + self.product.name + '-' + self.amount + '-' + self.check_amount


class StockDailyLog(models.Model):
    logged_on = models.DateField(_('logged_on'), auto_now=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                             null=False)
    product = models.ForeignKey(Product, related_name=_('stock_daily_log'),
                                blank=False, null=False)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2,
                                default=0.00)
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    max_amount = models.DecimalField(_('max_amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    min_amount = models.DecimalField(_('min_amount'), max_digits=9, decimal_places=2,
                                default=0.00)

    class Meta:
        ordering = ('logged_on', 'department', 'product',)
        index_together = ['logged_on', 'department', 'product',]
        unique_together = (('logged_on', 'department', 'product',))

    def __str__(self):
        return self.logged_on + '-' + self.department.name + '-' + self.product.name + '-' + self.amount


class StockUpdateLog(models.Model):
    logged_on = models.DateTimeField(_('logged_on'), auto_now=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                             null=False)
    product = models.ForeignKey(Product, related_name=_('stock_update_log'),
                                blank=False, null=False)
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    from_amount = models.DecimalField(_('from_amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    to_amount = models.DecimalField(_('to_amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    from_ip = models.GenericIPAddressField(_('from_ip'))
    host_name = models.CharField(max_length=30, blank=True, null=True)
    longitude = models.FloatField(_('longitude'), null=False, default=0, blank=True)
    latitude = models.FloatField(_('latitude'), null=False, default=0, blank=True)

    class Meta:
        ordering = ('logged_on', 'department', 'product',)
        index_together = ['logged_on', 'department', 'product',]
        unique_together = (('logged_on', 'department', 'product',))

    def __str__(self):
        return self.logged_on + '-' + self.department.name + '-' + self.product.name + '-' + self.amount
