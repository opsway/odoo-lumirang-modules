from datetime import datetime
from typing import Callable, Optional

from odoo import fields

from .timezone import as_server_timezone

TzCallbackType = Callable[[Optional[datetime]], Optional[datetime]]


class DatetimeWithTz(fields.Datetime):
    tz_callback: TzCallbackType

    _slots = {
        'tz_callback': None,
    }

    def __get__(self, instance, owner):
        value = super().__get__(instance, owner)
        if instance is None:
            return value
        if self.tz_callback:
            value = self.tz_callback(value)
        return value


class DatetimeWithServerTz(fields.Datetime):
    def __get__(self, instance, owner):
        value = super().__get__(instance, owner)
        if instance is None:
            return value
        value = as_server_timezone(instance.env, value)
        return value
