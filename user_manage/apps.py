from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UserManageConfig(AppConfig):
    label = 'User Manage'
    name = 'user_manage'
    verbose_name = _('User manage')
