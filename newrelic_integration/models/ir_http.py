from logging import WARNING
from odoo import models
from odoo.http import request

from ..lib.nr_init import init_agent
from ..lib.nr_logging import init_logging

_nr_initialized = False


def _init_nr(env):
    ir_param = env['ir.config_parameter'].sudo()
    if not ir_param.get_param('newrelic.is_enabled') or not env['res.config.settings'].has_newrelic():
        return
    key = ir_param.get_param('newrelic.license_key')
    company = env['res.company'].browse(1)
    init_agent(key, company.newrelic_config)
    if ir_param.get_param('newrelic.is_logging'):
        level = ir_param.get_param('newrelic.log_level')
        try:
            level = int(level)
        except (ValueError, TypeError):
            level = WARNING
        init_logging(level, key)


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls):
        result = super()._dispatch()
        global _nr_initialized
        if not _nr_initialized:
            try:
                import newrelic.agent
                _init_nr(request.env)
            except ImportError:
                pass
            _nr_initialized = True
        return result
