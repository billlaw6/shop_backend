from django.contrib import admin

from dict_manage.models import Category, Product


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'is_active', 'description', 'meta_keywords',
              'meta_description', 'created_by', 'updated_by']

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'brand', 'price', 'sale_price', 'is_active',
              'is_bestseller', 'description', 'meta_keywords', 'image',
              'meta_description', 'manufacturer', 'created_by', 'updated_by']

admin.site.register(Product, ProductAdmin)
