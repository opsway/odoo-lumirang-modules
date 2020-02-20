import pytz
from odoo import fields, models

TIMEZONES = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]


def _timezones(self):
    return TIMEZONES


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    timezone = fields.Selection(_timezones, string='Timezone', default=lambda self: self._context.get('tz'),
                                config_parameter='force_timezone.timezone')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['res.partner'].search([('id', "!=", 0)]).write({'tz': self.timezone})
