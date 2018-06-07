from django.conf.urls import url, include
from rest_framework import routers

from sale_manage import views
from sale_manage.views import (ProductViewSet, CategoryViewSet,
    StockViewSet, AddressViewSet)


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'categories', CategoryViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^order$', views.AddOrder.as_view(), name='order'),
]
