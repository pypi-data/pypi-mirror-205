from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.core.checks import register
from django.core.checks import Tags

from django_tsp.checks import check_settings


class DjangoTspConfig(AppConfig):
    name = 'django_tsp'
    label = 'django_tsp'
    verbose_name = _('Travel Salesman Problem Wrapper')

    def ready(self) -> None:
        register(Tags.security)(check_settings)