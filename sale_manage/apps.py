from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SaleManageConfig(AppConfig):
    label = 'Sale manage'
    name = 'sale_manage'
    verbose_name = _('Sale manage')
