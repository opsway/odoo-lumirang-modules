from odoo import api, models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    first_name = fields.Char(string="First name", related='partner_id.first_name', inherited=True, readonly=False)
    last_name = fields.Char(string="Last name", related='partner_id.last_name', inherited=True, readonly=False)

    @api.onchange('partner_id')
    def _onchange_partner(self):
        self.first_name, self.last_name, self.login = self.partner_id.first_name, self.partner_id.last_name, \
                                                      self.partner_id.email

    @api.model
    def create(self, values):
        res = super(ResUsers, self).create(values)
        if res.first_name:
            res.partner_id.write({
                'last_name': res.last_name,
                'first_name': res.first_name
            })
        return res
