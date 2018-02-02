import hashlib
import json
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from allauth.socialaccount.providers.weixin.client import WeixinOAuth2Client
from allauth.socialaccount.providers.weixin.views import WeixinOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from user_manage.serializers import UserSerializer

# Create your views here.


# ViewSets define the view behavior.
def home(request):
    return HttpResponse('Home')


class UserViewSet(viewsets.ModelViewSet):
    """
    The actions provided by the ModelViewSet class are .list(), .retrieve(),
    .create(), .update(), .partial_update(), and .destroy().
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class WeixinLogin(SocialLoginView):
    adapter_class = WeixinOAuth2Adapter

def weixin_token_check(request):
    token = 'carryon.top'
    timestamp = request.GET.get('timestamp', 'timestamp')
    nonce = request.GET.get('nonce', 'nonce')
    signature = request.GET.get('signature', 'signature')
    echostr = request.GET.get('echostr', 'echostr')
    tmp_arr = sorted([timestamp, nonce, token])
    tmp_str = ''.join(tmpArr)
    hash_str = hashlib.sha1(tmpStr.encode("utf8"))
    # print(hash_str.hexdigest())
    if signature == hashStr.hexdigest():
        return HttpResponse(echostr)
    else:
        return HttpResponse('no match')


def weixin_login(request):
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)
    if code and state:
        wx_client = WeixinOAuth2Client(request,
            'wx4a32725dfd171687',
            '14123aca2110ec62e097ab8c1cb2734d',
            'GET',
            'https://api.weixin.qq.com/sns/oauth2/access_token',
            'http://123.56.115.20/',
            'snsapi_userinfo')
        try:
            access_token_info = wx_client.get_access_token(code)
            access_token = json.load(access_token_info)
            print(type('type of access_token: %s' % access_token))
            print('access_token: %s ' % access_token['access_token'])
            return HttpResponse('got access_token: %s' % access_token['access_token'])
        except (Exception) as e:
            print(e)
            return HttpResponse('error')
    else:
        return HttpResponse('error')


