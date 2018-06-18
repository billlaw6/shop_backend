from django.test import TestCase

from user_manage.models import ShopUser


# Create your tests here.
class MyUserModelTests(TestCase):
    def my_user_crud_test(self):
        """
        测试MyUser模型的增删改查基础操作
        """
        test_user = ShopUser(username='test', password='test')
        test_user.save()

    def django_rest_auth_test(self):
        """
        测试自定义的用户模型及认证方式，结合djangorestframework获取Token登录,
        注销、
        """
        pass
