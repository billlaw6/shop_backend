from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from pypinyin import lazy_pinyin, Style
from rest_framework import serializers

from user_manage.models import (ShopUser,)
from sale_manage.models import (Order, Product,
    Category, ProductPicture, Express, Payment,
    OrderStatus, Location, Address, Order,
    OrderDetail, VisitLog, Stock, StockMoveRecord,
    StockCheck, StockDailyLog, StockUpdateLog)


# class ProductSerializer(serializers.HyperlinkedModelSerializer):
class ProductSerializer(serializers.ModelSerializer):
    # 一个产品对应多个库房的库存记录
    stock_record = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=Stock.objects.all())
    # 一个产品只对应一个创建人
    created_by = serializers.PrimaryKeyRelatedField(many=False, queryset=ShopUser.objects.all())
    updated_by = serializers.PrimaryKeyRelatedField(many=False, queryset=ShopUser.objects.all())
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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    user = serializers.ReadOnlyField(source='user.__str__')
    location = serializers.ReadOnlyField(source='location.__str__')
    class Meta:
        model = Address
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.__str__')
    class Meta:
        model = Order
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
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


# Serializers define the API representation.
# class ProductSerializer(serializers.HyperlinkedModelSerializer):

#     class Meta:
#         model = Product
#         fields = ('id', 'name', 'pinyin', 'py', 'brand', 'price', 'sale_price',
#                   'image', 'description', 'highlighted', 'updated_at', 'created_at')
