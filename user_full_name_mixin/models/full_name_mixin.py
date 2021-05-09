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
        if 'name' in values and ('last_name' in values or 'first_name' in values):
            # prefer name construction over decomposition, i.e. construct full name from parts if they are present:
            del values['name']
        elif not ('name' in values or 'last_name' in values or 'first_name' in values):
            raise ValidationError("First and last names are required")
        return super().create(values)
