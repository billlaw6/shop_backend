from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from pypinyin import lazy_pinyin, Style
from rest_framework import serializers

from user_manage.models import (ShopUser,)
from sale_manage.models import (Order, Product,
    Category, ProductPicture, Express, Payment,
    OrderStatus, Order,
    OrderDetail, VisitLog, Stock, StockMoveRecord,
    StockCheck, StockDailyLog, StockUpdateLog)


# class ProductSerializer(serializers.HyperlinkedModelSerializer):
class ProductSerializer(serializers.ModelSerializer):
    # 一个产品对应多个库房的库存记录
    stock_record = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=Stock.objects.all())
    # 一个产品只对应一个创建人
    created_by = serializers.PrimaryKeyRelatedField(many=False, queryset=ShopUser.objects.all())
    updated_by = serializers.PrimaryKeyRelatedField(many=False, queryset=ShopUser.objects.all())
    # created_by = serializers.ReadOnlyField(source='created_by.__str__')
    # updated_by = serializers.CharField(required=False, source='updated_by.__str__')
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        # fields = ("name",)


class ProductPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPicture
        fields = "__all__"


class ExpressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Express
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(required=False, source='product.name')
    class Meta:
        model = OrderDetail
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(required=False, source='created_by.__str__')
    buyer_name = serializers.ReadOnlyField(required=False, source='buyer.__str__')
    # 字段可为空时不要使用__str__函数，否则报错
    payment_name = serializers.ReadOnlyField(required=False, source='payment.name')
    address_name = serializers.ReadOnlyField(required=False, source='address.name')
    status_name = serializers.ReadOnlyField(required=False, source='status.__str__')
    # payment = serializers.StringRelatedField(required=False, many=False)
    # address = serializers.StringRelatedField(required=False, many=False)
    # status = serializers.StringRelatedField(required=False, many=False)
    # 名字和related_name一致才会包含在__all__中
    order_details = OrderDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = "__all__"


class VisitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitLog
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    department = serializers.ReadOnlyField(source='department.__str__')
    product = serializers.ReadOnlyField(source='product.__str__')
    class Meta:
        model = Stock
        fields = "__all__"


class StockMoveRecordSerializer(serializers.ModelSerializer):
    productName = serializers.ReadOnlyField(source='product.name')
    sale_price = serializers.ReadOnlyField(source='product.sale_price')

    class Meta:
        model = StockMoveRecord
        fields = "__all__"


class StockCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockCheck
        fields = "__all__"


class StockDailyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockDailyLog
        fields = "__all__"


class StockUpdateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockUpdateLog
        fields = "__all__"


# class OrderSerializer(serializers.Serializer):
#     sum_price = serializers.CharField(label=_("Sum price"),
#                                   style={'input_type': 'Number'})

#     def validate(self, attrs):
#         # sum_price = attrs.get('sum_price')
#         if sum_price:
#             user = authenticate(username=username, password=password)

#             if user:
#                 if not user.is_active:
#                     msg = _('User account is disabled.')
#                     raise serializers.ValidationError(msg)
#             else:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg)
#         else:
#             msg = _('Must include "username" and "password".')
#             raise serializers.ValidationError(msg)

#         attrs['user'] = user
#         return attrs

