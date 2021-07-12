from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG

try:
    import newrelic.agent as agent
except ImportError:
    agent = None

from odoo import fields, models, api

_LEVEL_TO_NAME = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
}

_log_levels = (
    CRITICAL,
    ERROR,
    WARNING,
    INFO,
    DEBUG,
)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_using_newrelic_js = fields.Boolean("NewRelic JS Wrapper", config_parameter='newrelic.is_js_enabled')
    is_newrelic_running = fields.Boolean("NewRelic running", readonly=True)
    is_using_newrelic = fields.Boolean("Enable NewRelic", config_parameter='newrelic.is_enabled')
    newrelic_license_key = fields.Char("License Key", config_parameter='newrelic.license_key')
    is_newrelic_logging = fields.Boolean("Send Logs", config_parameter='newrelic.is_logging')
    newrelic_log_level = fields.Selection([(str(x), _LEVEL_TO_NAME[x]) for x in _log_levels], "Log Level",
                                          default=str(WARNING), config_parameter='newrelic.log_level')

    @api.model
    def has_newrelic(self):
        return agent and agent.global_settings().monitor_mode

    @api.model
    def get_values(self):
        result = super().get_values()
        result['is_newrelic_running'] = self.has_newrelic()
        return result

    def open_newrelic_config(self):
        return {
            'type': 'ir.actions.act_window',
            'name': "NewRelic Config",
            'view_mode': 'form',
            'res_model': 'res.company',
            'res_id': self.env.company.id,
            'view_id': self.env.ref('newrelic_integration.view_newrelic_config').id,
            'target': 'new',
        }
