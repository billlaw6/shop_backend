import hashlib
# import json
from django.http import HttpResponse
from django.contrib.auth import get_user_model, logout as core_logout
from rest_framework import viewsets, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
# from social_django.models import UserSocialAuth

from user_manage.models import Department
from user_manage.serializers import (UserSerializer,
    DepartmentSerializer)

# Create your views here.


# ViewSets define the view behavior.
def home(request):
    user = request.user
    print('user: %s' % user)
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
