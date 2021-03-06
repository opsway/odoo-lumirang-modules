from odoo import models, fields, api
from odoo.exceptions import ValidationError

from ..lib.format import format_name


class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char(string="First name")
    last_name = fields.Char(string="Last name")

    name = fields.Char(string='Name', store=True, index=True, compute="_compute_name", inverse="_inverse_name")

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for partner in self:
            partner.name = format_name(partner.first_name, partner.last_name)

    def _inverse_name(self):
        for partner in self:
            if partner.is_company and format_name(partner.first_name, partner.last_name) != partner.name:
                partner.first_name = partner.name
                partner.last_name = ""

    @api.model
    def create(self, values: dict):
        if not values.get('name'):
            last_name = values.get('last_name')
            first_name = values.get('first_name')
            if first_name and last_name:
                values['name'] = format_name(first_name, last_name)
            else:
                raise ValidationError("First and last names are required")
        return super(ResPartner, self).create(values)
