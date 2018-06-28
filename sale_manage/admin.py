from django.contrib import admin
from sale_manage.models import (Category, Product, CategoryProductRelation,
ProductPicture, Express, Payment, OrderStatus, Order,
OrderDetail, VisitLog, Stock, StockMoveRecord, StockCheck, StockDailyLog,
StockUpdateLog)

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    # 不具体指名字段则全显示
    pass
    # fields = ['name', 'is_active', 'description', 'meta_keywords',
    #           'meta_description']

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    pass
    # fields = ['name', 'brand', 'price', 'sale_price', 'is_active',
    #           'is_bestseller', 'description', 'meta_keywords', 'image',
    #           'meta_description', 'manufacturer', 'created_by', 'updated_by']

admin.site.register(Product, ProductAdmin)


@admin.register(CategoryProductRelation)
class CategoryProductRelationAdmin(admin.ModelAdmin):
    # fields = ('category', 'product')
    pass

    def category(self, obj):
        return obj.name

    category.empty_value_display = '???'


@admin.register(ProductPicture)
class ProductPictureAdmin(admin.ModelAdmin):
    pass


@admin.register(Express)
class ExpressAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    pass


@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    pass


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(StockMoveRecord)
class StockMoveRecordAdmin(admin.ModelAdmin):
    pass


@admin.register(StockCheck)
class StockCheckAdmin(admin.ModelAdmin):
    pass


@admin.register(StockDailyLog)
class StockDailyLogAdmin(admin.ModelAdmin):
    pass

