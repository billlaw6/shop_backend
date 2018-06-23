# from django.shortcuts import render

# # Create your views here.

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import parsers, renderers, viewsets, permissions, authentication
from rest_framework.decorators import (api_view, throttle_classes,
    permission_classes, renderer_classes, parser_classes,
    authentication_classes,)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle

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


class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'

@api_view(['POST'])
# @renderer_classes(renderers.JSONRenderer,)
# @parser_classes([parsers.FormParser, parsers.MultiPartParser,
#                       parsers.JSONParser,])
# @throttle_classes([OncePerDayUserThrottle])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAdminUser])
def create_product(request, *args, **kwargs):
    """
    """
    serializer = ProductSerializer(data=request.data)
    print(serializer.initial_data)
    serializer.initial_data['created_by'] = request.user.id
    serializer.initial_data['updated_by'] = request.user.id
    if serializer.initial_data.get('file') != 'null':
        print("has file:")
        serializer.initial_data['image'] = serializer.initial_data['file']
    else:
        print("has no file:")
        serializer.initial_data.pop('image', None)
    if serializer.is_valid():
        print(serializer.validated_data)
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    else:
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
# @renderer_classes(renderers.JSONRenderer,)
# @parser_classes([parsers.FormParser, parsers.MultiPartParser,
#                       parsers.JSONParser,])
# @throttle_classes([OncePerDayUserThrottle])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAdminUser])
def update_product(request, *args, **kwargs):
    """
    """
    # print(request.data)
    # print(request.data.get('id'))
    # 如果带ID号，则更新原对象
    # aim_product = Product.objects.get(id=request.data.get('id'))
    aim_product = get_object_or_404(Product, pk=request.data.get('id'))
    request.data['created_by']=aim_product.created_by.id
    request.data['updated_by']=request.user.id
    serializer = ProductSerializer(aim_product, data=request.data, partial=True)
    serializer.initial_data.pop('stock_record', None)
    print('initial_data')
    print(serializer.initial_data)
    if (serializer.initial_data.get('file') is None) or (serializer.initial_data.get('file') == 'null'):
        print('has no file')
        serializer.initial_data.pop('image', None)
    else:
        print('has file:')
        serializer.initial_data['image'] = serializer.initial_data['file']
    if serializer.is_valid():
        print('validated_data')
        print(serializer.validated_data)
        result = serializer.update(aim_product, serializer.validated_data)
        print('updated: %s' % (result))
        return JsonResponse(serializer.data, status=201)
    else:
        print("invalid")
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
# @renderer_classes(renderers.JSONRenderer,)
# @parser_classes([parsers.FormParser, parsers.MultiPartParser,
#                       parsers.JSONParser,])
# @throttle_classes([OncePerDayUserThrottle])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAdminUser])
def toggle_product(request, *args, **kwargs):
    """
    """
    aim_product = get_object_or_404(Product, pk=request.data.get('id'))
    request.data['updated_by']=request.user.id
    if aim_product.is_active:
        Product.objects.filter(pk=aim_product.id).update(is_active=False)
    else:
        Product.objects.filter(pk=aim_product.id).update(is_active=True)
    return JsonResponse(ProductSerializer(aim_product).data, status=201, safe=False)


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

    def update(self, request, pk=None):
        print(request.data)
        print("Updating data")


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
