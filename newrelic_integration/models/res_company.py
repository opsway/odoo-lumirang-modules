import os

from odoo import fields, models


def default_newrelic_config(*arg, **kw):
    with open(os.path.dirname(os.path.abspath(__file__)) + '/newrelic.dist.ini') as file:
        return "".join(file.readlines())


class ResCompany(models.Model):
    _inherit = 'res.company'

    newrelic_config = fields.Text(default=default_newrelic_config)
