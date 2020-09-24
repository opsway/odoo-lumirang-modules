from datetime import datetime
from typing import Optional, Any

import pytz
from odoo import fields
from odoo.models import Model

from ..lib.timezone import as_timezone


class ResPartner(Model):
    _inherit = 'res.partner'

    def timezone_option(self) -> str:
        """
        Return server timezone.
        :return:
        """
        return self.env['ir.config_parameter'].sudo().get_param('force_timezone.timezone', default=pytz.utc.zone)

    tz = fields.Selection(default=timezone_option)

    def as_user_timezone(self, dt: Optional[datetime], default: Any = False) -> datetime:
        """
        Convert UTC timezone to the user timezone.
        :param dt: timezone-unaware datetime instance to convert in UTC timezone
        :param default: fallback value for absent datetime instance
        :return: timezone-aware datetime in user's timezone
        """
        return as_timezone(dt, self.env['res.partner'].tz, default)
