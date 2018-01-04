# from django.shortcuts import render

# # Create your views here.

from rest_framework import parsers, renderers
from rest_framework.response import Response
from rest_framework.views import APIView

from sale_manage.models import Order
from sale_manage.serializer import OrderSerializer


class AddOrder(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,
                      parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Order.objects.get_or_create(user=user)
        return Response({'token': token.key})


add_order = AddOrder.as_view()
