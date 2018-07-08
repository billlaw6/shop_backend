from django.conf.urls import url, include
from rest_framework import routers

from sale_manage import views


router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, base_name='product')
router.register(r'stocks', views.StockViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'expresses', views.ExpressViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'move-records', views.StockMoveRecordViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^order/add/$', views.add_order, name='order'),
    url(r'^order/process/$', views.process_order, name='process-order'),
    url(r'^order-detail/toggle/$', views.toggle_order_detail, name='toggle_order_detail'),
    url(r'^product/create/$', views.create_product, name='create_product'),
    url(r'^product/update/$', views.update_product, name='update_product'),
    url(r'^product/toggle/$', views.toggle_product, name='toggle_product'),
    url(r'^move-record/add/$', views.add_move_record, name='add_move_record'),
    url(r'^move-record/process/$', views.process_move_record, name='process_move_record'),
    url(r'^move-record/$', views.get_stock_move_record, name='stock_move_record'),
    url(r'^stock/$', views.get_stock, name='stock'),
]
