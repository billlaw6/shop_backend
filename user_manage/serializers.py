from django.contrib.auth import get_user_model
from rest_framework import serializers

from user_manage.models import (Group, Department, DictEmployeeRank,
      DictEmployeeStatus, DictSex, DictUserStatus )
from sale_manage.models import (Order)


# Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = get_user_model()
        # 如果添加url，必须有shopuser-detail名的url配置
        # fields = "__all__"
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'department', 'is_staff', 'is_superuser', 'orders')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DictEmployeeRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictEmployeeRank
        fields = "__all__"


class DictEmployeeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictEmployeeStatus
        fields = "__all__"


class DictSexSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictSex
        fields = "__all__"


class DictUserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictUserStatus
        fields = "__all__"
