from django.contrib.auth import get_user_model
from rest_framework import viewsets

from dict_manage.serializers import UserSerializer

# Create your views here.


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
