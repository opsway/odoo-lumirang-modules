from datetime import datetime

import pytz
from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(IrHttp, self).session_info()
        res['force_timezone'] = self.env['res.partner'].timezone_option()
        tz = pytz.timezone(res['force_timezone'])
        offset = tz.utcoffset(datetime.now())
        res['force_timezone_minutes'] = (offset.days * 86400 + offset.seconds) // 60
        return res
