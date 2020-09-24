from datetime import datetime
from typing import Optional, Any

import pytz


def as_timezone(dt: Optional[datetime], to_tz: str, default: Any = False) -> datetime:
    """
    Convert UTC timezone to the specified one.
    :param dt: timezone-unaware datetime instance to convert in UTC timezone
    :param to_tz: destination timezone
    :param default: fallback value for absent datetime instance
    :return: timezone-aware datetime in the specified timezone
    """
    if not dt:
        return default
    tz_local = pytz.timezone(to_tz)
    return dt.replace(tzinfo=pytz.UTC).astimezone(tz_local)


def as_server_timezone(env, dt: Optional[datetime], default: Any = False) -> datetime:
    """
    Convert UTC timezone to the server default.
    :param env: odoo environment
    :param dt: timezone-unaware datetime instance to convert in UTC timezone
    :param default: fallback value for absent datetime instance
    :return: timezone-aware datetime in the server timezone
    """
    return as_timezone(dt, env['res.partner'].timezone_option(), default)
