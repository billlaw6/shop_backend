from django.contrib.auth import get_user_model
from rest_framework import serializers

from user_manage.models import (Group, Department, DictEmployeeRank,
      Address, Location,
      DictEmployeeStatus, DictSex, DictUserStatus )
from sale_manage.models import (Order)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


# Serializers define the API representation.
# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.ModelSerializer):
    # orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())
    # department = DepartmentSerializer()
    dept_belong = DepartmentSerializer(many=True, read_only=True)
    group_belong = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        # 如果添加url，必须有shopuser-detail名的url配置
        # fields = "__all__"
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'dept_belong', 'group_belong', 'is_staff', 'is_superuser')


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


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    user = serializers.ReadOnlyField(source='user.__str__')
    location = serializers.ReadOnlyField(source='location.__str__')
    class Meta:
        model = Address
        fields = "__all__"


class DictUserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictUserStatus
        fields = "__all__"
