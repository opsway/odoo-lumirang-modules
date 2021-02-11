from odoo import models, fields, api
from odoo.exceptions import ValidationError

from ..lib.format import format_name, decompose_name


class FullNameMixin(models.AbstractModel):
    _name = 'full.name.mixin'

    first_name = fields.Char(string="First name")
    last_name = fields.Char(string="Last name")

    name = fields.Char(string='Name', store=True, index=True, compute="_compute_name", inverse="_inverse_name")

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for partner in self:
            partner.name = format_name(partner.first_name, partner.last_name)

    def _inverse_name(self):
        for partner in self:
            partner.first_name, partner.last_name = decompose_name(partner.name)

    @api.model
    def create(self, values: dict):
        if not values.get('name'):
            last_name = values.get('last_name')
            first_name = values.get('first_name')
            if first_name and last_name:
                values['name'] = format_name(first_name, last_name)
            else:
                raise ValidationError("First and last names are required")
        elif not values.get('first_name') and not values.get('last_name'):
            names = decompose_name(values['name'])
            values['first_name'] = names[0]
            values['last_name'] = names[-1]
        return super().create(values)
