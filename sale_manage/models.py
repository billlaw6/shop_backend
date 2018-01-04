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
from django.contrib.auth.models import User
from django.utils import timezone
from pypinyin import lazy_pinyin, Style


class Order(models.Model):
    order_no = models.CharField(max_length=50, unique=True, blank=True,
                                default='')
    sum_amount = models.PositiveSmallIntegerField(_('sum_amount'), null=False,
                                                  default=0)
    sum_price = models.DecimalField(_('sum_price'), max_digits=9,
                                    decimal_places=2, blank=False,
                                    null=False, default=0.00)
    payment = models.ForeignKey(Payment, related_name=_('orders'),
                                to_field='code', blank=False, null=False)
    buyer = models.CharField(_('buyer'), max_length=100, blank=False,
                             null=False, default='zhangsan')
    cell_phone = models.CharField(_('cell_phone'), max_length=15, null=False,
                                  default='', blank=True)
    city = models.CharField(_('city'), max_length=200, blank=False, null=False)
    address = models.CharField(_('address'), max_length=300, blank=False,
                               default='')
    comment = models.CharField(_('comment'), max_length=300, blank=True,
                               default='')
    status = models.ForeignKey(OrderStatus, related_name=_('orders'),
                               default=1)
    express = models.ForeignKey(Express, related_name=_('orders'),
                                to_field='code', null=False, default='')
    express_no = models.CharField(_('express_no'), max_length=50,
                                  blank=True, null=False, default='')
    express_info = models.TextField(
                                    _('express_info'),
                                    blank=True, null=False, default='')
    created_at = models.DateTimeField(
                                      _('created_at'),
                                      blank=True, default=timezone.now)

    class Meta:
        ordering = ('created_at',)
        index_together = ['order_no', 'created_at', 'express_no']
        unique_together = (('cell_phone', 'address', 'comment'))

    def __str__(self):
        return self.order_no + '-' + self.buyer + '-' + str(self.cell_phone)

    # def save(self, *args, **kwargs):
    #     """
    #     city字段array型数据单独处理
    #     """
    #     city = json.dumps(self.city)
    #     super(Order, self).save(*args, **kwargs)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name=_(
        'order_detail'), blank=False, null=False)
    submerchandise = models.ForeignKey(Product, related_name=_(
        'order_details'), blank=False, null=False)
    name = models.CharField(_('name'), max_length=100)
    amount = models.PositiveSmallIntegerField(_('amount'), null=False,
                                              default=1)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2,
                                default=0.00)
    created_at = models.DateTimeField(_('created_at'), blank=True,
                                      default=timezone.now)


class VisitLog(models.Model):
    from_ip = models.GenericIPAddressField(_('from_ip'))
    visit_url = models.URLField(_('visit_url'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, default='')
    visit_date = models.DateTimeField(null=False, default='')
    browser = models.CharField(
        _('browser'),
        max_length=64,
        null=False, default='',
        blank=True)
    longitude = models.FloatField(
        _('longitude'),
        null=False, default=0, blank=True)
    latitude = models.FloatField(
        _('latitude'),
        null=False,
        default=0,
     blank=True)

    class Meta:
        ordering = ('visit_date', 'from_ip',)
        verbose_name = _('VisitLog')
        verbose_name_plural = _('VisitLogs')

    def __str__(self):
        return self.user.username + '-' + self.from_ip + '-' + self.visit_date


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name=_('comments'),
                                blank=False, null=False,
                                on_delete=models.CASCADE)
    cell_phone = models.CharField(
                                  _('cell_phone'),
                                  max_length=15,
                                  null=False,
                                  default='',
                                  blank=True)
    author = models.CharField(_('author'), max_length=100)
    content = models.TextField(_('content'), blank=True, null=False, default='')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.cell_phone + '-' + self.name + '-' + self.content
