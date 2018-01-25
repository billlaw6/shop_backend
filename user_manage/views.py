from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from allauth.socialaccount.providers.weixin.views import WeixinOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from user_manage.serializers import UserSerializer

# Create your views here.


# ViewSets define the view behavior.
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
