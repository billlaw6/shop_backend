# from django.shortcuts import render

# # Create your views here.

from rest_framework import parsers, renderers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from sale_manage.models import (Order, Product,
    Category, ProductPicture, Express, Payment,
    OrderStatus, Location, Address, Order,
    OrderDetail, VisitLog, Stock, StockMoveRecord,
    StockCheck, StockDailyLog, StockUpdateLog)
from sale_manage.serializers import (OrderSerializer, ProductSerializer,
    CategorySerializer, ProductPictureSerializer, ExpressSerializer,
    PaymentSerializer, OrderStatusSerializer, LocationSerializer,
    AddressSerializer, OrderSerializer, OrderDetailSerializer,
    VisitLogSerializer, StockSerializer, StockMoveRecordSerializer,
    StockCheckSerializer, StockDailyLogSerializer, StockUpdateLogSerializer)


class AddOrder(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,
                      parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Order.objects.get_or_create(user=user)
        return Response({'token': token.key})

add_order = AddOrder.as_view()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProductPictureViewSet(viewsets.ModelViewSet):
    queryset = ProductPicture.objects.all()
    serializer_class = ProductPictureSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ExpressViewSet(viewsets.ModelViewSet):
    queryset = Express.objects.all()
    serializer_class = ExpressSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class OrderStatusViewSet(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # The create() method of our serializer will now be passed an additional 'owner' field, along with the validated data from the request.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
