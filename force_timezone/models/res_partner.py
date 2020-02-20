import pytz
from odoo import fields
from odoo.models import Model


class ResPartner(Model):
    _inherit = 'res.partner'

    def timezone_option(self):
        return self.env['ir.config_parameter'].sudo().get_param('force_timezone.timezone', default=pytz.utc.zone)

    tz = fields.Selection(default=timezone_option)
