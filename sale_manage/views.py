# from django.shortcuts import render

# # Create your views here.

from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.db.models import Q
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import parsers, renderers, viewsets, permissions, authentication
from rest_framework.decorators import (api_view, throttle_classes,
    permission_classes, renderer_classes, parser_classes,
    authentication_classes,)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
import re, datetime, json

from sale_manage.models import (Order, Product,
    Category, ProductPicture, Express, Payment,
    OrderStatus, Order,
    OrderDetail, VisitLog, Stock, StockMoveRecord,
    StockCheck, StockDailyLog, StockUpdateLog)
from sale_manage.serializers import (OrderSerializer, ProductSerializer,
    CategorySerializer, ProductPictureSerializer, ExpressSerializer, PaymentSerializer, OrderStatusSerializer, OrderSerializer, OrderDetailSerializer,
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
        return JsonResponse(serializer.errors, status=303)

@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAuthenticatedOrReadOnly,])
def search_product(request, *args, **kwargs):
    """
    """
    keyword = request.GET.get('keyword', '')
    limit = request.GET.get('limit', 10)
    offset = request.GET.get('offset', 0)
    print('%s-%s-%s' % (keyword, limit, offset))
    if limit and offset:
        if keyword is None:
            queryset = Product.objects.all()[int(offset): int(offset)+int(limit)]
        else:
          queryset = Product.objects.filter(Q(pinyin__icontains=keyword)
              | Q(py__icontains=keyword)
              | Q(name__icontains=keyword))[int(offset): int(offset)+int(limit)]
    else:
        queryset = Product.objects.all()
    res_data = {}
    res_data['count'] = len(queryset)
    res_data['results'] = ProductSerializer(queryset, many=True).data
    return Response(res_data, status=200)


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
        return JsonResponse(serializer.errors, status=303)


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
    # 默认为购物车状态
    order['status'] = 'cart'
    if request.data.get('customer') is not None:
        order['buyer'] = request.data.get('customer').get('id')
        order['status'] = 'submited'
    if request.data.get('cartListSum') is not None:
        order['sum_price'] = request.data.get('cartListSum')
    if request.data.get('express') is not None:
        order['express'] = request.data.get('express').get('id')
        order['status'] = 'sent'
    if request.data.get('payment') is not None:
        order['payment'] = request.data.get('payment').get('id')
        order['status'] = 'checked'
    if request.data.get('status') is not None:
        order['status'] = request.data.get('status')

# transaction 方式二
# with transaction.atomic():
    order_serializer = OrderSerializer(data=order)
    # print(order_serializer.initial_data)
    if order_serializer.is_valid() and (request.data.get('cartList')) == 0:
        # print(order_serializer.validated_data)
        new_order = order_serializer.save()
        # print(new_order)
    else:
        # print('order invalid')
        # print(order_serializer.errors)
        return JsonResponse(order_serializer.errors, status=303)
    for item in request.data.get('cartList'):
        item['order'] = new_order.order_no
        # print(item)
        item['product'] = item['id']
        item['amount'] = item['amount']
        detail_serializer = OrderDetailSerializer(data=item)
        if detail_serializer.is_valid():
            # print('validated_data')
            # print(detail_serializer.validated_data)
            result = detail_serializer.save()
        else:
            # print("invalid")
            # print(detail_serializer.errors)
            return JsonResponse(detail_serializer.errors, status=303)
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
    # print(request.data)
    if (request.data.get('order_no') and request.data.get('status')):
        params = {}
        if (request.data.get('express', '') != ''):
            params['express'] = request.data.get('express')
            params['status'] = 'sent'
        if (request.data.get('express_no', '') != ''):
            params['express_no'] = request.data.get('express_no')
        if (request.data.get('payment', '') != ''):
            params['payment'] = request.data.get('payment')
            params['status'] = 'checked'
        if (request.data.get('comment', '') != ''):
            params['comment'] = request.data.get('comment')
        if (request.data.get('status', '') == 'trashed'):
            order = Order.objects.filter(pk=request.data.get('order_no'))
            # print(order[0].status)
            if order[0].status.code in ('cart', 'submited',):
                order.update(status='trashed')
                return Response('trashed', status=203)
            else:
                return Response('no process', status=204)

        order = Order.objects.filter(pk=request.data.get('order_no'))
        # 减库存
        for item in OrderDetail.objects.filter(order_id=request.data.get('order_no')):
            aim = Stock.objects.filter(department=order[0].department.code, product=item.product.id)
            # print("aim: %s" % aim)
            if len(aim) > 0:
                if aim[0].amount >= item.amount:
                    aim.update(amount=aim[0].amount - item.amount)
                else:
                    return Response('notEnoughStock', status=204)
            else:
                return Response('noStock', status=204)
            # print(params)
            # 更新订单状态
            order.update(**params)
            return Response(params['status'], status=203)
    else:
        return Response('no order no or no status', status=303)


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
def search_stock_move_record(request, *args, **kwargs):
    now = datetime.datetime.now()
    delt = datetime.timedelta(days=3)
    start = request.GET.get('start', (now-delt).strftime('%Y-%m-%d %H:%M:%S'))
    end  = request.GET.get('end', now.strftime('%Y-%m-%d %H:%M:%S'))
    department = request.GET.get('department', None)
    offset = request.GET.get('offset', 0)
    limit = request.GET.get('limit', 10)
    if department is None:
        return Response('no department', status=203)
    # print('paras: %s|%s|%s|%s|%s' % (department, start, end, offset, limit))
    queryset = StockMoveRecord.objects.filter(
        Q(entered_on__gte=start) & Q(entered_on__lte=end),
        Q(dept_out=department) | Q(dept_in=department)
      )[int(offset): int(offset)+int(limit)]
    # print(queryset)
    # 如果不是一级库房，不取状态为0，接收单位为自己的数据
    source_dept_re = re.compile(r'^1\d{4}')
    if not source_dept_re.match(department):
        queryset = StockMoveRecord.objects.filter(
            Q(entered_on__gte=start) & Q(entered_on__lte=end),
            Q(dept_out=department) | Q(dept_in=department)
          ).exclude(
            Q(dept_in=department) & Q(status=0)
          )[int(offset): int(offset)+int(limit)]
    res_data = {}
    res_data['count'] = len(queryset)
    res_data['results'] = StockMoveRecordSerializer(queryset, many=True).data
    return Response(res_data, status=200)


@api_view(['GET'])
# @renderer_classes([renderers.JSONRenderer,])
# @authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAuthenticatedOrReadOnly,])
def search_stock(request, *args, **kwargs):
    department = request.GET.get('department', None)
    if department is None:
        Response('no department', status=203)
    keyword = request.GET.get('keyword', '')
    limit = request.GET.get('limit', 10)
    offset = request.GET.get('offset', 0)
    # print('%s-%s-%s-%s' % (department, keyword, limit, offset))
    rs_product = Product.objects.filter(
        Q(pinyin__icontains=keyword) |
        Q(py__icontains=keyword) |
        Q(name__icontains=keyword)
    )
    p_id = [p.id for p in rs_product]
    queryset = Stock.objects.filter(
        Q(department_id=department),
        product_id__in=p_id
    )[int(offset): int(offset)+int(limit)]
    res_data = {}
    res_data['count'] = len(queryset)
    res_data['results'] = StockSerializer(queryset, many=True).data
    return Response(res_data, status=200)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAdminUser])
@transaction.atomic
def add_move_record(request, *args, **kwargs):
    """
    """
    dept_out = request.data.get('deptOut', None)
    dept_in = request.data.get('deptIn', None)
    record_list = request.data.get('moveRecordList', None)
    if record_list is None or len(record_list) == 0:
        return Response('no content', status=303)
    if dept_in is None:
        return Response('no dept_in', status=303)
    page_no = utils._generate_order_no()
    for item in record_list:
        # print(item)
        # print(type(item))
        # print(item['product']['sale_price'])
        item['page_no'] = page_no
        item['price'] = item['product']['sale_price']
        item['product'] = item['product']['id']
        item['batch_no'] = item['batchNo']
        item['move_amount'] = item['moveAmount']
        # 只有一级库房才可以录入的入库单，并且是采购单
        item['dept_out'] = dept_out['code'] if dept_out['code'] else '00001'
        item['dept_in'] = dept_in['code']
        item['entered_by'] = request.user.id
        serializer = StockMoveRecordSerializer(data=item)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            print("invalid")
            print(serializer.errors)
            return JsonResponse(serializer.errors, status=303)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAdminUser])
@transaction.atomic
def process_move_record(request, *args, **kwargs):
    """
    """
    # print(request.data)
    aim = StockMoveRecord.objects.filter(pk=request.data.get('id', 0))
    current_department = request.data.get('currentDept', None)
    if current_department is None:
        return Response('no current department', status=303)
    # 当前库房为接收库房
    if current_department['code'] == aim[0].dept_in.code:
        stock_records = Stock.objects.filter(department=aim[0].dept_in.code, product=aim[0].product.id, batch_no=aim[0].batch_no)
        if aim[0].dept_out.level == 0:
            # 如果发出库房为采购源且状态为0，加库存或建账页
            if aim[0].status == 0:
                if len(stock_records) > 0:
                    print('in exists')
                    stock_records.update(amount = stock_records[0].amount + aim[0].move_amount)
                    aim.update(status = 1)
                    return Response('OK', status=203)
                else:
                    print('in not exists')
                    new_data = {}
                    new_data['department'] = aim[0].dept_in.code
                    # 根据Serializer中字段类型选择
                    # new_data['product_id'] = aim[0].product.id
                    new_data['product'] = aim[0].product.id
                    new_data['batch_no'] = aim[0].batch_no
                    new_data['amount'] = aim[0].move_amount
                    print('new_data: %s' % new_data)
                    new_serializer = StockSerializer(data = new_data)
                    if new_serializer.is_valid():
                        print('validated_data: %s' % new_serializer.validated_data)
                        aim.update(status = 1)
                        new_stock = new_serializer.save()
                        if new_stock:
                            return Response('OK', status=201)
                        else:
                            return Response('create stock failed', status=303)
                    else:
                        print(new_serializer.errors)
                        return JsonResponse(new_serializer.errors, status=303)
            # 状态为1是已接收，处理成结算状态
            elif aim[0].status == 1:
                aim.update(status = 2)
                return Response('OK', status=203)
        else:
            # 如果发出库房非采购源且状态为0，接收方不显示，发出方处理成出库待接收状态。
            if aim[0].status == 0:
                return Response('no process', status=204)
            # 状态为1,则是其它库房已发出待自己接收的单子，加库存并修改状态至已接收。
            elif aim[0].status == 1:
                if len(stock_records) > 0:
                    print('in exists')
                    stock_records.update(amount = stock_records[0].amount + aim[0].move_amount)
                    aim.update(status = 2)
                    return Response('OK', status=203)
                else:
                    print('in not exists')
                    new_data = {}
                    new_data['department'] = aim[0].dept_in.code
                    # new_data['product'] = model_to_dict(aim[0].product, exclude=['image',])
                    new_data['product'] = aim[0].product.id
                    new_data['batch_no'] = aim[0].batch_no
                    new_data['amount'] = aim[0].move_amount
                    print('new_data: %s' % new_data)
                    new_serializer = StockSerializer(data = new_data)
                    if new_serializer.is_valid():
                        print('validated_data: %s' % new_serializer.validated_data)
                        aim.update(status = 2)
                        new_stock = new_serializer.save()
                        if new_stock:
                            return Response('OK', status=201)
                        else:
                            return Response('create stock failed', status=303)
                    else:
                        print(new_serializer.errors)
                        return JsonResponse(new_serializer.errors, status=303)
    # 当前库房为发出库房
    elif current_department['code'] == aim[0].dept_out.code:
        # 当前库房为出库库房，且当前状态为0，减库存
        if aim[0].status == 0:
            stock_records = Stock.objects.filter(department=aim[0].dept_out.code, product=aim[0].product.id, batch_no=aim[0].batch_no)
            if len(stock_records) > 0:
                if stock_records[0].amount - aim[0].move_amount > 0:
                    stock_records.update(amount = stock_records[0].amount - aim[0].move_amount)
                    aim.update(status = 1)
                    return Response('OK', status=203)
                else:
                    return Response('not enough stock', status=303)
            else:
                return Response('no stock', status=303)
        # 当前状态为1,由接收方处理，发出方只显示不处理。
        elif aim[0].status == 1:
            return Response('no process', status=204)
