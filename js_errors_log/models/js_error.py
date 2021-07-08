from odoo import models, fields


class JsErrorType(models.Model):
    _name = 'js.error.type'
    name = fields.Char()


class JsError(models.Model):
    _name = 'js.error'
    _order = "create_date desc"

    error_type_id = fields.Many2one('js.error.type')
    name = fields.Char(related='error_type_id.name')
    user_id = fields.Many2one('res.users')
    message = fields.Text()
    data = fields.Text()
