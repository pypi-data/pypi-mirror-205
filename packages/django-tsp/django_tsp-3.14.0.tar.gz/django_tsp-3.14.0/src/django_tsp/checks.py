from collections.abc import Sequence
from typing import Any

from django.conf import settings
from django.core.checks import CheckMessage
from django.core.checks import Error

from django_tsp.conf import conf


def check_settings(**kwargs: Any) -> list[CheckMessage]:
    errors: list[CheckMessage] = []

    if not is_sequence(conf.NAME_LIST, str):
        errors.append(
            Error(
                "NAME_LIST should be a sequence of strings.",
                id="django_tsp.E001",
            )
        )

    if not isinstance(conf.COMPANY_NAME, str):
        errors.append(
            Error("COMPANY_NAME should be a string.", id="django_tsp.E009")
        )

    if hasattr(settings, "REQ_NAME"):
        errors.append(
            Error(
                (
                    "The REQ_NAME setting has been removed"
                    + " - see django_tsp' CHANGELOG."
                ),
                id="django_tsp.E013",
            )
        )

    return errors

def is_sequence(thing: Any, type_or_types: type[Any] | tuple[type[Any], ...]) -> bool:
    return isinstance(thing, Sequence) and all(
        isinstance(x, type_or_types) for x in thing
    )