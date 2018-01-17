from rest_framework import serializers

from dict_manage.models import Product


# Serializers define the API representation.
class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'pinyin', 'py', 'brand', 'price', 'sale_price',
                  'description', 'highlighted')
