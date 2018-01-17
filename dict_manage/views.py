from rest_framework import viewsets

from dict_manage.models import Product
from dict_manage.serializers import ProductSerializer

# Create your views here.


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
