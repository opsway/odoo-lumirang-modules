try:
    import newrelic.agent as agent
except ImportError:
    agent = None

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_using_newrelic = fields.Boolean("NewRelic", config_parameter='newrelic.is_enabled')
    is_newrelic_running = fields.Boolean("NewRelic running", readonly=True)

    @api.model
    def has_newrelic(self):
        return agent and agent.global_settings().monitor_mode

    @api.model
    def get_values(self):
        result = super().get_values()
        result['is_newrelic_running'] = self.has_newrelic()
        return result
