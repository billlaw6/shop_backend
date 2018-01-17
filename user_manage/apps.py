from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UserManageConfig(AppConfig):
    # 应用的缩写名称，默认是name的最后部分，例如'admin'
    label = 'user_manage'
    # 应用的完整Python 路径，例如django.contrib.admin
    name = 'user_manage'
    # 应用的适合阅读的名称，例如“Administration”
    verbose_name = _('User manage')
