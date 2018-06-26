from django.conf.urls import url, include
from rest_framework import routers

from sale_manage import views


router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, base_name='product')
router.register(r'stocks', views.StockViewSet)
router.register(r'addresses', views.AddressViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'expresses', views.ExpressViewSet)
router.register(r'payments', views.PaymentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^order/add/$', views.add_order, name='order'),
    url(r'^product/create/$', views.create_product, name='create_product'),
    url(r'^product/update/$', views.update_product, name='update_product'),
    url(r'^product/toggle/$', views.toggle_product, name='toggle_product'),
]
