from django.conf.urls import url, include
from rest_framework import routers

from user_manage import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'addresses', views.AddressViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^home', views.home, name='home'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^logged-out$', views.logged_out, name='logged_out'),
    url(r'^weixin-check', views.weixin_token_check, name='weixin_check'),
    url(r'^user-info', views.UserInfo.as_view(), name='user_info'),
    url(r'^user-perms', views.UserPermissions.as_view(), name='user_perms'),
]
