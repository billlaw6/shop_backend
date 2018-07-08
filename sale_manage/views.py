# from django.shortcuts import render

# # Create your views here.

from django.http import HttpResponse, JsonResponse
from django.db import transaction
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
    OrderStatus, Order,
    OrderDetail, VisitLog, Stock, StockMoveRecord,
    StockCheck, StockDailyLog, StockUpdateLog)
from sale_manage.serializers import (OrderSerializer, ProductSerializer,
    CategorySerializer, ProductPictureSerializer, ExpressSerializer,
    PaymentSerializer, OrderStatusSerializer,
    OrderSerializer, OrderDetailSerializer,
    VisitLogSerializer, StockSerializer, StockMoveRecordSerializer,
    StockCheckSerializer, StockDailyLogSerializer, StockUpdateLogSerializer)
from sale_manage import utils
from sale_manage import permissions as my_perms
import uuid


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
    if (serializer.initial_data.get('file') is None) or (serializer.initial_data.get('file') == 'null'):
        print("has no file:")
        serializer.initial_data.pop('image', None)
    else:
        print("has file:")
        serializer.initial_data['image'] = serializer.initial_data['file']
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


@api_view(['POST'])
# @renderer_classes(renderers.JSONRenderer,)
# @parser_classes([parsers.FormParser, parsers.MultiPartParser,
#                       parsers.JSONParser,])
# @throttle_classes([OncePerDayUserThrottle])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAdminUser])
# transaction 方式一
@transaction.atomic
def add_order(request, *args, **kwargs):
    """
    """
    order = {}
    order['order_no'] = utils._generate_order_no()
    # order['order_no'] = str(uuid.uuid4())
    order['created_by'] = request.user.id
    if request.data.get('department') is not None:
        order['department'] = request.data.get('department')
    else:
        order['department'] = '20001'
    if request.data.get('customer') is not None:
        order['buyer'] = request.data.get('customer').get('id')
    if request.data.get('cartListSum') is not None:
        order['sum_price'] = request.data.get('cartListSum')
    if request.data.get('payment') is not None:
        order['payment'] = request.data.get('payment').get('id')
    if request.data.get('express') is not None:
        order['express'] = request.data.get('express').get('id')
    if request.data.get('status') is not None:
        order['status'] = request.data.get('status')
    else:
        order['status'] = 'submited'

# transaction 方式二
# with transaction.atomic():
    order_serializer = OrderSerializer(data=order)
    print(order_serializer.initial_data)
    if order_serializer.is_valid():
        # print(order_serializer.validated_data)
        new_order = order_serializer.save()
        # print(new_order)
    else:
        # print('order invalid')
        print(order_serializer.errors)
        return JsonResponse(order_serializer.errors, status=400)
    for item in request.data.get('cartList'):
        item['order'] = new_order.order_no
        print(item)
        item['product'] = item['id']
        item['amount'] = item['amount']
        detail_serializer = OrderDetailSerializer(data=item)
        if detail_serializer.is_valid():
            print('validated_data')
            print(detail_serializer.validated_data)
            result = detail_serializer.save()
        else:
            print("invalid")
            print(detail_serializer.errors)
            return JsonResponse(detail_serializer.errors, status=400)
    return JsonResponse(order_serializer.data, status=201)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([my_perms.IsAdminOrOwner,])
@transaction.atomic
def process_order(request):
    print(request.data)
    if (request.data.get('order_no') and request.data.get('status')):
        params = {}
        if (request.data.get('express', '') != ''):
            params['express'] = request.data.get('express')
        if (request.data.get('express_no', '') != ''):
            params['express_no'] = request.data.get('express_no')
        if (request.data.get('payment', '') != ''):
            params['payment'] = request.data.get('payment')
        if (request.data.get('comment', '') != ''):
            params['comment'] = request.data.get('comment')

        order = Order.objects.filter(pk=request.data.get('order_no'))
        if (request.data.get('status', '') == 'cart'):
            params['status'] = 'order'
            order.update(**params)
            return Response(params['status'], status=203)
        elif (request.data.get('status', '') in ['submited', 'sent']):
            if (request.data.get('express', '') != ''):
                params['status'] = 'sent'
                # 减库存
                for item in OrderDetail.objects.filter(order_id=request.data.get('order_no')):
                    print(order[0].department.code)
                    print(item.product.id)
                    aim = Stock.objects.filter(department=order[0].department.code, product=item.product.id)
                    print(aim)
                    if len(aim) > 0:
                        if aim[0].amount >= item.amount:
                            aim.update(amount=aim[0].amount - item.amount)
                        else:
                            print('inc')
                            return Response('insufficient', status=303)
                    else:
                        print('nostock')
                        return Response('no stock', status=303)
            if (request.data.get('payment', '') != ''):
                params['status'] = 'checked'
            else:
                params['status'] = request.data.get('status')
            Order.objects.filter(pk=request.data.get('order_no')).update(**params)
            return Response(params['status'], status=203)
        elif (request.data.get('status', '') in ['checked', 'trashed']):
            return Response('no process', status=203)
        else:
            return Response('error', status=303)
    else:
        return Response('error', status=303)


def toggle_order_detail(request, *args, **kwargs):
    """
    """
    aim = get_object_or_404(OrderDetail, pk=request.data.get('id'))
    request.data['updated_by']=request.user.id
    if aim.status == 0:
        Product.objects.filter(pk=aim.id).update(
            status=1,
            updated_by=request.user
          )
    elif aim.status == 1:
        Product.objects.filter(pk=aim.id).update(
            status=0,
            updated_by=request.user
          )
    return JsonResponse(OrderDetailSerializer(aim).data, status=201, safe=False)


class OrderStatusViewSet(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # permission_classes = (permissions.AllowAny,)

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


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StockMoveRecordViewSet(viewsets.ModelViewSet):
    queryset = StockMoveRecord.objects.all()
    serializer_class = StockMoveRecordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


@api_view(['GET'])
# @renderer_classes([renderers.JSONRenderer,])
# @authentication_classes([authentication.TokenAuthentication,])
# @permission_classes([permissions.IsAdminUser])
def get_stock_move_record(request, *args, **kwargs):
    print(request.data)
    department = request.data.get('department', None)
    if (request.data.get('offset', None)) and (request.data.get('limit', None)):
        start = request.data.get('offset', None)
        end = start + request.data.get('limit', None)
        if department is None:
            queryset = StockMoveRecord.objects.all()[start:end]
        else:
          queryset = StockMoveRecord.objects.filter(department=department)[start:end]
    else:
        if department is None:
            queryset = StockMoveRecord.objects.all()
        else:
          queryset = StockMoveRecord.objects.filter(department=department)
    print(queryset)
    return Response(StockMoveRecordSerializer(queryset, many=True).data, status='200')


@api_view(['GET'])
# @renderer_classes([renderers.JSONRenderer,])
# @authentication_classes([authentication.TokenAuthentication,])
# @permission_classes([permissions.IsAdminUser])
def get_stock(request, *args, **kwargs):
    # print(request.data)
    print(request.GET.get('department', ''))
    department = request.GET.get('department', None)
    if (request.GET.get('offset', None)) and (request.GET.get('limit', None)):
        start = request.GET.get('offset', None)
        end = start + request.GET.get('limit', None)
        if department is None:
            queryset = Stock.objects.all()[start:end]
        else:
          queryset = Stock.objects.filter(department=department)[start:end]
    else:
        if department is None:
            queryset = Stock.objects.all()
        else:
          queryset = Stock.objects.filter(department=department)
    res_data = {}
    res_data['count'] = len(queryset)
    res_data['results'] = StockSerializer(queryset, many=True).data
    return Response(res_data, status='200')


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAdminUser])
@transaction.atomic
def add_move_record(request, *args, **kwargs):
    """
    """
    # print(request.data)
    for item in request.data.get('moveRecordList'):
        if (request.data.get('dept_out', '') == ''):
            item['dept_out'] = '00001'
        item['dept_in'] = request.data.get('dept_in')
        item['entered_by'] = request.user.id
        # print(item)
        serializer = StockMoveRecordSerializer(data=item)
        if serializer.is_valid():
            # print('validated_data')
            # print(serializer.validated_data)
            serializer.save()
        else:
            # print("invalid")
            # print(serializer.errors)
            return JsonResponse(serializer.errors, status=400)
    return JsonResponse(serializer.data, status=201)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAdminUser])
@transaction.atomic
def process_move_record(request, *args, **kwargs):
    """
    """
    print(request.data)
    data = StockMoveRecord.objects.get(pk=request.data.get('id', 0))
    print(data)
    stock_records = Stock.objects.filter(department=data.dept_in, product=data.product.id, batch_no=data.batch_no)
    if len(stock_records) > 0:
        print('exists')
        stock_records.update(amount = stock_records[0].amount + data.move_amount)
    else:
        print('not exists')
        new_data = {}
        print(data.dept_in.code)
        new_data['department'] = data.dept_in.code
        new_data['product'] = data.product.id
        new_data['batch_no'] = data.batch_no
        new_data['amount'] = data.move_amount
        new_serializer = StockSerializer(data = new_data)
        if new_serializer.is_valid():
            print(new_serializer.validated_data)
            new_serializer.save()
        else:
            return JsonResponse(new_serializer.errors, status=400)
    return Response('OK', status=203)
