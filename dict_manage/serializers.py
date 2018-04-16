from rest_framework import serializers

from dict_manage.models import Product


# Serializers define the API representation.
class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'pinyin', 'py', 'brand', 'price', 'sale_price',
                  'image', 'description', 'highlighted')
