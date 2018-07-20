import hashlib
# import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model, logout as core_logout
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, authentication, permissions
from rest_framework.decorators import (api_view, throttle_classes,
    permission_classes, renderer_classes, parser_classes,
    authentication_classes,)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
# from social_django.models import UserSocialAuth

from user_manage.models import Department, Address, Location
from user_manage.serializers import (UserSerializer,
    AddressSerializer, LocationSerializer,
    DepartmentSerializer)

# Create your views here.


# ViewSets define the view behavior.
def home(request):
    user = request.user
    # print('user: %s' % user)
    # social_accounts = UserSocialAuth.objects.filter(id=user.id)
    # print(social_accounts[0].extra_data)
    # return HttpResponse(social_accounts[0].extra_data)
    return HttpResponse('user :%s' % user.username)


def logout(request):
    # 千万别重名，否则死循环
    core_logout(request)
    return HttpResponse('logged out')


def logged_out(request):
    return HttpResponse('logged out')


def weixin_token_check(request):
    """
    纯用于微信服务器校验
    """
    token = 'carryon.top'
    timestamp = request.GET.get('timestamp', 'timestamp')
    nonce = request.GET.get('nonce', 'nonce')
    signature = request.GET.get('signature', 'signature')
    echostr = request.GET.get('echostr', 'echostr')
    tmp_arr = sorted([timestamp, nonce, token])
    tmp_str = ''.join(tmp_arr)
    hash_str = hashlib.sha1(tmp_str.encode("utf8"))
    # print(hash_str.hexdigest())
    if signature == hash_str.hexdigest():
        return HttpResponse(echostr)
    else:
        return HttpResponse('no match')


class UserViewSet(viewsets.ModelViewSet):
    """
    The actions provided by the ModelViewSet class are .list(), .retrieve(),
    .create(), .update(), .partial_update(), and .destroy().
    """
    queryset = get_user_model().objects.filter(is_active=1)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    The actions provided by the ModelViewSet class are .list(), .retrieve(),
    .create(), .update(), .partial_update(), and .destroy().
    """
    queryset = Department.objects.filter(is_active=1)
    # queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserInfo(APIView):
    """
    返回当前登录用户信息
    * Require token authentication.
    * Only authenticated users are able to access thie view
    """
    authentication_classes = (authentication.SessionAuthentication,
                              authentication.TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(JSONRenderer().render(serializer.data))


class UserPermissions(APIView):
    """
    返回当前登录用户的权限
    """
    authentication_classes = (authentication.SessionAuthentication,
                              authentication.TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        perms = JSONRenderer().render(request.user.get_all_permissions())
        return Response(perms)


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


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAuthenticated,])
def search_customer(request, *args, **kwargs):
    """
    """
    keyword = request.GET.get('keyword', '')
    limit = request.GET.get('limit', 10)
    offset = request.GET.get('offset', 0)
    # print('%s-%s-%s' % (keyword, limit, offset))
    if limit and offset:
        if keyword is None:
            queryset = get_user_model().objects.all()[int(offset): int(offset)+int(limit)]
        else:
          queryset = get_user_model().objects.filter(Q(username__icontains=keyword)
              | Q(cell_phone__icontains=keyword)
              | Q(last_name__icontains=keyword)
              | Q(first_name__icontains=keyword))[int(offset): int(offset)+int(limit)]
    else:
        queryset = get_user_model().objects.all()
    res_data = {}
    res_data['count'] = len(queryset)
    res_data['results'] = UserSerializer(queryset, many=True).data
    return Response(res_data, status=200)


@api_view(['POST'])
# @renderer_classes(renderers.JSONRenderer,)
# @parser_classes([parsers.FormParser, parsers.MultiPartParser,
#                       parsers.JSONParser,])
# @throttle_classes([OncePerDayUserThrottle])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAdminUser])
def create_customer(request, *args, **kwargs):
    """
    """
    serializer = UserSerializer(data=request.data)
    serializer.initial_data['created_by'] = request.user.id
    serializer.initial_data['updated_by'] = request.user.id
    if serializer.is_valid():
        # print(serializer.validated_data)
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    else:
        # print(serializer.errors)
        return JsonResponse(serializer.errors, status=303)

@api_view(['POST'])
# @renderer_classes(renderers.JSONRenderer,)
# @parser_classes([parsers.FormParser, parsers.MultiPartParser,
#                       parsers.JSONParser,])
# @throttle_classes([OncePerDayUserThrottle])
@authentication_classes([authentication.TokenAuthentication,])
@permission_classes([permissions.IsAdminUser])
def update_customer(request, *args, **kwargs):
    """
    """
    # print(request.data)
    # print(request.data.get('id'))
    # 如果带ID号，则更新原对象
    # aim_customer = Customer.objects.get(id=request.data.get('id'))
    aim_customer = get_object_or_404(get_user_model(), pk=request.data.get('id'))
    request.data['updated_by']=request.user.id
    serializer = UserSerializer(aim_customer, data=request.data, partial=True)
    # print(serializer.initial_data)
    if serializer.is_valid():
        # print('validated_data')
        # print(serializer.validated_data)
        result = serializer.update(aim_customer, serializer.validated_data)
        # print('updated: %s' % (result))
        return JsonResponse(serializer.data, status=201)
    else:
        # print("invalid")
        # print(serializer.errors)
        return JsonResponse(serializer.errors, status=303)
