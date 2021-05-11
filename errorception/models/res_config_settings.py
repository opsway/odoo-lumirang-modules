from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_using_errorception = fields.Boolean("ErrorCeption", config_parameter='errorception.is_enabled')
    errorception_key = fields.Char(config_parameter='errorception.access_key')
