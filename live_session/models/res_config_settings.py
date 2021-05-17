from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_using_live_session = fields.Boolean("LiveSession", config_parameter='live_session.is_enabled')
    live_session_key = fields.Char(config_parameter='live_session.access_key')
    live_session_type = fields.Selection(selection=[
        (x, x,) for x in ('Frontend', 'Both',)
    ], config_parameter='live_session.type', default='Both')
