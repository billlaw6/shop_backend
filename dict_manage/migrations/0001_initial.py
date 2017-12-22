# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-22 02:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('pinyin', models.CharField(blank=True, default='', max_length=50)),
                ('py', models.CharField(blank=True, default='', max_length=50)),
                ('is_active', models.BooleanField(default=False, verbose_name='is_active')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('meta_keywords', models.CharField(blank=True, default='', help_text='Comma-delimited set of                                      SEO keywords for meta tag', max_length=255, verbose_name='meta keywords')),
                ('meta_description', models.CharField(blank=True, default='', help_text='Content for description                                         meta tag', max_length=255, verbose_name='meta description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated_at')),
                ('highlighted', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_categories', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updated_categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell_phone', models.CharField(blank=True, default='', max_length=15, verbose_name='cell_phone')),
                ('author', models.CharField(max_length=100, verbose_name='author')),
                ('content', models.TextField(blank=True, default='', verbose_name='content')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Express',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='code')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('pinyin', models.CharField(blank=True, default='', max_length=50)),
                ('py', models.CharField(blank=True, default='', max_length=50)),
                ('is_active', models.BooleanField(default=False, verbose_name='is_active')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_region_code', models.CharField(max_length=10, verbose_name='country_region_code')),
                ('country_region_name', models.CharField(max_length=30, verbose_name='country_region_name')),
                ('country_region_py_code', models.CharField(blank=True, default='', max_length=30, verbose_name='country_region_py_code')),
                ('country_region_quanpin', models.CharField(blank=True, default='', max_length=200, verbose_name='country_region_quanpin')),
                ('state_code', models.CharField(blank=True, default='', max_length=10, verbose_name='state_code')),
                ('state_name', models.CharField(blank=True, default='', max_length=30, verbose_name='state_name')),
                ('state_py_code', models.CharField(blank=True, default='', max_length=100, verbose_name='state_py_code')),
                ('state_quanpin', models.CharField(blank=True, default='', max_length=200, verbose_name='state_quanpin')),
                ('city_code', models.CharField(blank=True, default='', max_length=10, verbose_name='city_code')),
                ('city_name', models.CharField(blank=True, default='', max_length=30, verbose_name='city_name')),
                ('city_py_code', models.CharField(blank=True, default='', max_length=100, verbose_name='city_py_code')),
                ('city_quanpin', models.CharField(blank=True, default='', max_length=200, verbose_name='city_quanpin')),
                ('region_code', models.CharField(blank=True, default='', max_length=10, verbose_name='region_code')),
                ('region_name', models.CharField(blank=True, default='', max_length=30, verbose_name='region_name')),
                ('region_py_code', models.CharField(blank=True, default='', max_length=100, verbose_name='region_py_code')),
                ('region_quanpin', models.CharField(blank=True, default='', max_length=200, verbose_name='region_quanpin')),
                ('longitude', models.FloatField(blank=True, default=0.0, verbose_name='longitude')),
                ('latitude', models.FloatField(blank=True, default=0.0, verbose_name='latitude')),
                ('detail_location', models.CharField(blank=True, default='', max_length=200, verbose_name='detail_location')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='code')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('pinyin', models.CharField(blank=True, default='', max_length=50)),
                ('py', models.CharField(blank=True, default='', max_length=50)),
                ('is_active', models.BooleanField(default=False, verbose_name='is_active')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='code')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('pinyin', models.CharField(blank=True, default='', max_length=50)),
                ('py', models.CharField(blank=True, default='', max_length=50)),
                ('is_active', models.BooleanField(default=False, verbose_name='is_active')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('pinyin', models.CharField(blank=True, default='', max_length=50)),
                ('py', models.CharField(blank=True, default='', max_length=50)),
                ('brand', models.CharField(blank=True, default='', max_length=50, verbose_name='brand')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='price')),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, verbose_name='sale_price')),
                ('is_active', models.BooleanField(default=False, verbose_name='is_active')),
                ('is_bestseller', models.BooleanField(default=False, verbose_name='is_bestseller')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('meta_keywords', models.CharField(blank=True, default='', help_text='Comma-delimited set of                                      SEO keywords for meta tag', max_length=255, verbose_name='meta keywords')),
                ('meta_description', models.CharField(blank=True, default='', help_text='Content for description                                         meta tag', max_length=255, verbose_name='meta description')),
                ('manufacturer', models.CharField(blank=True, default='', max_length=300, verbose_name='manufacturer')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated_at')),
                ('highlighted', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_products', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updated_products', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProductPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('pinyin', models.CharField(blank=True, default='', max_length=50)),
                ('py', models.CharField(blank=True, default='', max_length=50)),
                ('image', models.ImageField(upload_to='product_photo', verbose_name='image')),
                ('order', models.PositiveSmallIntegerField(default=1, verbose_name='order')),
                ('description', models.TextField(blank=True, default='', verbose_name='description')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created_at')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='dict_manage.Product')),
            ],
            options={
                'ordering': ('product', 'order'),
            },
        ),
        migrations.CreateModel(
            name='VisitLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_ip', models.GenericIPAddressField(verbose_name='from_ip')),
                ('visit_url', models.URLField(verbose_name='visit_url')),
                ('visit_date', models.DateTimeField(default='')),
                ('browser', models.CharField(blank=True, default='', max_length=64, verbose_name='browser')),
                ('longitude', models.FloatField(blank=True, default=0, verbose_name='longitude')),
                ('latitude', models.FloatField(blank=True, default=0, verbose_name='latitude')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('visit_date', 'from_ip'),
                'verbose_name_plural': 'VisitLogs',
                'verbose_name': 'VisitLog',
            },
        ),
        migrations.AlterIndexTogether(
            name='location',
            index_together=set([('country_region_code', 'state_code', 'city_code', 'region_code')]),
        ),
        migrations.AddField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='dict_manage.Product'),
        ),
    ]
