from odoo import models, fields, api


class CustomMessageWizard(models.TransientModel):
    _name = 'custom_message.wizard'
    _description = "Custom Message Wizard"

    text = fields.Text('Message', readonly=True)

    @api.model
    def message_action(self, text, title="Notification"):
        wizard_id = self.create({'text': text})
        return {
            'name': title,
            'type': "ir.actions.act_window",
            'view_mode': 'form',
            'res_model': 'custom_message.wizard',
            'res_id': wizard_id.id,
            'target': 'new'
        }
