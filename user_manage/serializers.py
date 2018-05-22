from django.contrib.auth import get_user_model
from rest_framework import serializers


# Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        # 如果添加url，必须有shopuser-detail名的url配置
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_superuser')
