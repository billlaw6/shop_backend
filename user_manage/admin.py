from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from user_manage.models import ShopUser


# Register your models here.
class ShopUserAdmin(admin.ModelAdmin):
    fields = ['username', 'email', 'first_name', 'last_name',
              'cell_phone', 'expired_on', 'is_staff',
              'is_superuser', 'is_active', 'date_joined', 'last_login']

# admin.site.unregister(User)
admin.site.register(get_user_model(), ShopUserAdmin)
