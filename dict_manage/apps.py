from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DictManageConfig(AppConfig):
    label = 'Dict manage'
    name = 'dict_manage'
    verbose_name = _('Dict manage')
