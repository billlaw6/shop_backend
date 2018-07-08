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
from datetime import date
from pypinyin import lazy_pinyin, Style
from user_manage.models import Department, Address


class Product(models.Model):
    # code = models.CharField(_('code'), unique=True, max_length=64)
    name = models.CharField(_('name'), unique=True, max_length=128)
    pinyin = models.CharField(max_length=64, blank=True, null=False, default='')
    py = models.CharField(max_length=64, blank=True, null=False, default='')
    effective_month = models.IntegerField(blank=True, null=True)
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
    updated_by = models.ForeignKey(get_user_model(), models.SET_NULL,
                   related_name='updated_products', blank=True, null=True)
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
        models.SET_NULL,
        related_name='manager',
        blank=True,
        null=True
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
        return '%s-%s' % (self.product.name, self.name)


class Express(models.Model):
    code = models.CharField(_('code'), primary_key=True, max_length=64)
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
    code = models.CharField(_('code'), primary_key=True, max_length=64)
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
    code = models.CharField(_('code'), primary_key=True, max_length=128)
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


class Order(models.Model):
    order_no = models.CharField(max_length=64, unique=True, blank=True,
                                primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                            related_name=_('orders'), null=False)
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
                               default='cart') # 默认为购物车状态
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
        unique_together = (('buyer', 'order_no'))

    def __str__(self):
        return '%s-%s-%s' % (self.order_no, self.buyer.username, self.sum_price)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name=_('order_details'),
                                blank=False, null=False)
    product = models.ForeignKey(Product, related_name=_('order_detail'),
                                blank=False, null=False)
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2,
                                default=0.00)
    comment = models.CharField(_('comment'), max_length=300, blank=True,
                               default='')
    status = models.IntegerField(blank=False, null=False, default=0)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
        index_together = ['order', 'product']
        unique_together = (('order', 'product'))

    def __str__(self):
        return '%s-%s' % (self.order.order_no, self.product.name)


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
        return '%s-%s' % (self.visit_date, self.from_ip)


class Stock(models.Model):
    """库存管理到批次"""
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                            related_name=_('stock_record'), null=False)
    product = models.ForeignKey(Product, related_name=_('stock_record'),
                                blank=False, null=False)
    produced_at = models.DateField(_('produced_at'), blank=False, null=False, default=date.today)
    batch_no = models.CharField(_('batch_no'), max_length=128, blank=True, null=False, default='')
    amount = models.DecimalField(_('amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    max_amount = models.DecimalField(_('max_amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    min_amount = models.DecimalField(_('min_amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    location = models.CharField(max_length=256, blank=True, null=True)
    comment = models.CharField(max_length=256, blank=True, null=True)
    is_active = models.BooleanField(_('is_active'), default=False)

    class Meta:
        ordering = ('department', 'product',)
        index_together = ['department', 'product',]
        unique_together = (('department', 'product', 'batch_no',))

    def __str__(self):
        return '%s-%s-%s' % (self.department.name, self.product.name, self.batch_no)


class StockMoveRecord(models.Model):
    page_no = models.CharField(max_length=64, unique=True, blank=True,
                                default='')
    product = models.ForeignKey(Product, related_name=_('stock_move_record'),
                                blank=False, null=False)
    produced_at = models.DateField(_('produced_at'), blank=False, null=False, default=date.today)
    batch_no = models.CharField(_('batch_no'), max_length=128, blank=True, null=False, default='')
    dept_out = models.ForeignKey(Department, on_delete=models.CASCADE,
                             related_name='out_stock_move_records', null=True)
    dept_in = models.ForeignKey(Department, on_delete=models.CASCADE,
                             related_name='in_stock_move_records', null=False)
    move_amount = models.DecimalField(_('move_amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    in_result_amount = models.DecimalField(_('in_result_amount'), max_digits=9, decimal_places=2,
                                default=0.00)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2,
                                default=0.00)
    entered_on = models.DateTimeField(_('entered_on'), auto_now=True)
    entered_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                            related_name='entered_stock_move_records', null=False)
    processed_on = models.DateTimeField(_('processed_on'), blank=True, null=True)
    processed_by = models.ForeignKey(get_user_model(), models.SET_NULL,
                            related_name='processed_stock_move_records', null=True)
    # 采购记录需要结算
    checked_on = models.DateTimeField(_('checked_on'), blank=True, null=True)
    checked_by = models.ForeignKey(get_user_model(), models.SET_NULL,
                            related_name='checked_stock_move_records', null=True)
    status = models.IntegerField(blank=False, null=False, default=0)
    comment = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ('dept_in', 'dept_out', 'status', 'page_no', 'product',)
        index_together = ['page_no', 'dept_in',]
        unique_together = (('page_no', 'dept_in', 'dept_out', 'product', 'batch_no',))

    def __str__(self):
        return '%s-%s-%s-%s' % (self.dept_in.name, self.page_no, self.product.name, self.move_amount)


class StockCheck(models.Model):
    page_no = models.CharField(max_length=64, unique=True, blank=True,
                                default='')
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                             null=False)
    product = models.ForeignKey(Product, related_name=_('stock_check_record'),
                                blank=False, null=False)
    produced_at = models.DateField(_('produced_at'), blank=False, null=False, default=date.today)
    batch_no = models.CharField(_('batch_no'), max_length=128, blank=True, null=False, default='')
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
    checked_by = models.ForeignKey(get_user_model(), models.SET_NULL,
        related_name=_('checked_stock_check_records'), null=True)

    class Meta:
        ordering = ('department', 'page_no', 'product', 'status', )
        index_together = ['page_no', 'department',]
        unique_together = (('page_no', 'department', 'product', 'batch_no',))

    def __str__(self):
        return '%s-%s-%s-%s' % (self.department.name, self.page_no, self.product.name, self.amount, self.check_amount)


class StockDailyLog(models.Model):
    logged_on = models.DateField(_('logged_on'), auto_now=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                             null=False)
    product = models.ForeignKey(Product, related_name=_('stock_daily_log'),
                                blank=False, null=False)
    produced_at = models.DateField(_('produced_at'), blank=False, null=False, default=date.today)
    batch_no = models.CharField(_('batch_no'), max_length=128, blank=True, null=False, default='')
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
        unique_together = (('logged_on', 'department', 'product', 'batch_no'))

    def __str__(self):
        return '%s-%s-%s-%s' % (self.logged_on, self.department.name, self.product.name, self.amount)


class StockUpdateLog(models.Model):
    logged_on = models.DateTimeField(_('logged_on'), auto_now=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                             null=False)
    product = models.ForeignKey(Product, related_name=_('stock_update_log'),
                                blank=False, null=False)
    produced_at = models.DateField(_('produced_at'), blank=False, null=False, default=date.today)
    batch_no = models.CharField(_('batch_no'), max_length=128, blank=True, null=False, default='')
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
        unique_together = (('logged_on', 'department', 'product', 'batch_no'))

    def __str__(self):
        return '%s-%s-%s-%s' % (self.logged_on, self.department.name, self.product.name, self.amount)
