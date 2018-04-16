"""shop_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
# from rest_framework.authtoken import views as rest_views
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

# from user_manage.views import UserViewSet
from dict_manage.views import ProductViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
schema_view = get_schema_view(title='Shop API')

urlpatterns = [
    # Django urls
    url(r'^admin/', admin.site.urls),

    # REST_FRAMEWORK urls
    url(r'^rest-api/', include(router.urls)),
    # coreapi url
    url(r'^schema/$', schema_view),
    # REST api 浏览登录注销页面http://www.django-rest-framework.org/#installation
    url(r'^api-auth/', include('rest_framework.urls')),
    # http://www.django-rest-framework.org/api-guide/authentication/
    # url(r'^api-token-auth/', rest_views.obtain_auth_token),
    # django-rest-auth
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    # Django_rest_framework_social_oauth2
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),

    # Entry URL Vue combine
    # url(r'^$', TemplateView.as_view(template_name="index.html")),

    # My urls
    url(r'^user_manage/', include('user_manage.urls')),
    url(r'^utils/', include('verify_utils.urls')),
    url(r'^weixin/', include('weixin.urls')),
]
