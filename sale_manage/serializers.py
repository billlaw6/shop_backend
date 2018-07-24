# 展示Stock时想展示product对象明细，如果直接把product的read_only设置为True，会尝试生成新的Product
# 所以只好将read_only设置成默认的False，然后人工定义create函数
# 重写create好像不管用，所以非特别需要尽量不用nested serializer，
# 需要取的字段另外添加，反向用related_name关联的除外，因为不涉及此问题。
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from pypinyin import lazy_pinyin, Style
from rest_framework import serializers

from user_manage.models import (ShopUser,)
# from user_manage.serializers import (DepartmentSerializer,)
from sale_manage.models import (Order, Product,
    Category, ProductPicture, Express, Payment,
    OrderStatus, Order,
    OrderDetail, VisitLog, Stock, StockMoveRecord,
    StockCheck, StockDailyLog, StockUpdateLog)


# class ProductSerializer(serializers.HyperlinkedModelSerializer):
class ProductSerializer(serializers.ModelSerializer):
    # 一个产品对应多个库房的库存记录
    # stock_records = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=Stock.objects.all())
    # 一个产品只对应一个创建人
    stock_records = serializers.StringRelatedField(many=True, read_only=True) # 非Product本身字段，不涉及create问题。
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


class OrderDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(required=False, source='product.name')
    class Meta:
        model = OrderDetail
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(required=False, source='department.name')
    created_by_name = serializers.ReadOnlyField(required=False, source='created_by.__str__')
    buyer_name = serializers.ReadOnlyField(required=False, source='buyer.__str__')
    # 字段可为空时不要使用__str__函数，否则报错
    payment_name = serializers.ReadOnlyField(required=False, source='payment.name')
    express_name = serializers.ReadOnlyField(required=False, source='express.name')
    address_name = serializers.ReadOnlyField(required=False, source='address.name')
    status_name = serializers.ReadOnlyField(required=False, source='status.__str__')
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
    department_name = serializers.ReadOnlyField(source='department.name')
    product_name = serializers.ReadOnlyField(source='product.name')
    product_sale_price = serializers.ReadOnlyField(source='product.sale_price')
    # 如果这么写，生成数据时product就需要为字典型，并且生成Stock时会同时生成Product
    product_pinyin = serializers.ReadOnlyField(source='product.pinyin')
    product_py = serializers.ReadOnlyField(source='product.py')
    # product = ProductSerializer(many=False, read_only=False)  # 此模式新建Stock时会同时要新建Product
    # product_id = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Product.objects.all())
    class Meta:
        model = Stock
        fields = "__all__"
    # http://www.django-rest-framework.org/api-guide/relations/
    # 展示Stock时想展示product对象明细，如果直接把product的read_only设置为True，会尝试生成新的Product
    # 所以只好将read_only设置成默认的False，然后人工定义create函数
    # 重写create好像不管用，所以非特别需要尽量不用nested serializer，需要取的字段另外添加。
    # def save(self, validated_data):
    # def create(self, validated_data):
    #     print('save')
    #     print(validated_data)
    #     product_data = validated_data.pop('product')
    #     # validated_data['product'] = product_data.id
    #     stock = Stock.objects.create(**validated_data)
    #     return stock

class StockMoveRecordSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_py = serializers.ReadOnlyField(source='product.py')
    dept_in_name = serializers.ReadOnlyField(source='dept_in.name')
    dept_out_name = serializers.ReadOnlyField(source='dept_out.name')
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

