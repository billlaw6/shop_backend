from django.conf.urls import url, include
from rest_framework import routers

from sale_manage import views
from sale_manage.views import (ProductViewSet, CategoryViewSet,
    StockViewSet, AddressViewSet)


router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, base_name='product')
router.register(r'stocks', StockViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'categories', CategoryViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^order/$', views.add_order, name='order'),
    url(r'^product/create/$', views.create_product, name='create_product'),
    url(r'^product/update/$', views.update_product, name='update_product'),
    url(r'^product/toggle/$', views.toggle_product, name='toggle_product'),
]
