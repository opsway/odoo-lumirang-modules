from odoo import models, fields, api

CUSTOM_MESSAGE_WIZARD_MODEL = 'custom_message.wizard'


class CustomMessageWizard(models.TransientModel):
    _name = CUSTOM_MESSAGE_WIZARD_MODEL

    text = fields.Text('Message', readonly=True)

    @api.model
    def message_action(self, text, title="Notification"):
        wizard_id = self.create({'text': text})
        return {
            'name': title,
            'type': "ir.actions.act_window",
            'view_mode': 'form',
            'res_model': CUSTOM_MESSAGE_WIZARD_MODEL,
            'res_id': wizard_id.id,
            'target': 'new'
        }
