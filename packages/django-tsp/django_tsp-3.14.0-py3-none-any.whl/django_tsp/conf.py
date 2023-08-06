from django.conf import settings
from typing import Sequence
from django_tsp.defaults import default_names


class Settings:
    """
    Shadow Django's settings with a little logic
    """
    @property
    def NAME_LIST(self) -> Sequence[str]:
        return getattr(settings, "NAME_LIST", default_names)

    @property
    def COMPANY_NAME(self) -> str:
        return getattr(settings, "CORS_PREFLIGHT_MAX_AGE", "CoolBlue")

conf = Settings()