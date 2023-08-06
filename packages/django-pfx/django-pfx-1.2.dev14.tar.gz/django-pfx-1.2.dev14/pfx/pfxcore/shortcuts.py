
import logging
from datetime import date

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


def f(tmpl, **kwargs):
    return tmpl.format(**kwargs)


def get_object(queryset, related_field=None, **kwargs):
    from .exceptions import ModelNotFoundAPIError, RelatedModelNotFoundAPIError
    try:
        return queryset.get(**kwargs)
    except ObjectDoesNotExist:
        if related_field:
            raise RelatedModelNotFoundAPIError(related_field, queryset.model)
        raise ModelNotFoundAPIError(queryset.model)


def get_pk(obj):
    if isinstance(obj, dict) and 'pk' in obj:
        return obj['pk']
    return obj


def is_null(value):
    return not value or value.lower() in ('null', 'undefined')


def parse_int(value):
    if is_null(value):
        return None
    return int(value)


def get_int(data, key, default=None):
    if key not in data:
        return default
    try:
        return parse_int(data.get(key))
    except ValueError:
        from pfx.pfxcore.exceptions import APIError
        raise APIError(f(_("{key} must be an integer value."), key=key))


def parse_float(value):
    if is_null(value):
        return None
    return float(value)


def get_float(data, key, default=None):
    if key not in data:
        return default
    try:
        return parse_float(data.get(key))
    except ValueError:
        from pfx.pfxcore.exceptions import APIError
        raise APIError(f(_("{key} must be an float value."), key=key))


def parse_date(value):
    if is_null(value):
        return None
    return date.fromisoformat(value)


def get_date(data, key, default=None):
    if key not in data:
        return default
    try:
        return parse_date(data.get(key))
    except ValueError:
        from pfx.pfxcore.exceptions import APIError
        raise APIError(f(_("{key} must be a date value."), key=key))


def parse_bool(value):
    if is_null(value):
        return None
    if value.lower() in ('true', '1'):
        return True
    if value.lower() in ('false', '0'):
        return False
    raise ValueError(f"{value} is not a valid boolean value.")


def get_bool(data, key, default=None):
    if key not in data:
        return default
    try:
        return parse_bool(data.get(key))
    except ValueError:
        from pfx.pfxcore.exceptions import APIError
        raise APIError(f(
            _("{key} must be 'true'|'false'|'1'|'0' or empty."),
            key=key))


def delete_token_cookie(response):
    response.delete_cookie(
        'token',
        domain=settings.PFX_COOKIE_DOMAIN,
        samesite=settings.PFX_COOKIE_SAMESITE or 'None')
    return response
