from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from user_manage.models import (ShopUser, Group,
    Address, Location, GroupShopUserRelation,
    Department, DictEmployeeRank,
    DictEmployeeStatus, DictSex,
    DictUserStatus)
# DepartmentShopUserRelation)



# Register your models here.
class ShopUserAdmin(admin.ModelAdmin):
    fields = ['username', 'email', 'first_name', 'last_name',
              'cell_phone', 'expired_on', 'is_staff', 'department',
              'is_superuser', 'is_active', 'date_joined', 'last_login',
              'user_permissions']

# admin.site.unregister(User)
admin.site.register(get_user_model(), ShopUserAdmin)


class GroupAdmin(admin.ModelAdmin):
    fields = ['code', 'name', 'pinyin', 'py']

admin.site.register(Group, GroupAdmin)


@admin.register(GroupShopUserRelation)
class GroupShopUserRelationAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(DictEmployeeRank)
class DictEmployeeRankAdmin(admin.ModelAdmin):
    pass


@admin.register(DictEmployeeStatus)
class DictEmployeeStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(DictSex)
class DictSexAdmin(admin.ModelAdmin):
    pass


@admin.register(DictUserStatus)
class DictUserStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


# @admin.register(DepartmentShopUserRelation)
# class DeparmentShopUserRelationAdmin(admin.ModelAdmin):
#     pass
