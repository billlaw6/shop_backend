from django.conf.urls import url, include
from rest_framework import routers

from user_manage import views
from user_manage.views import (UserViewSet, DepartmentViewSet)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', views.home, name='home'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^logged-out$', views.logged_out, name='logged_out'),
    url(r'^weixin-check', views.weixin_token_check, name='weixin_check'),
    url(r'^user-info', views.UserInfo.as_view(), name='user_info'),
    url(r'^user-perms', views.UserPermissions.as_view(), name='user_perms'),
]
