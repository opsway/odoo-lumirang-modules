from odoo import models


class TestFullName(models.Model):
    _name = 'full.name.test.mixin'
    _inherit = ['full.name.mixin']
    _description = "Tests: Full name mixin test model"
