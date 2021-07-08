from odoo import models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def unlink(self):
        for attachment in self:
            name = attachment.name.lower()
            if attachment.res_model == 'ir.ui.view' and attachment.res_id == 0 and \
                    (name.endswith(".js") or name.endswith(".css")):
                self.env['obsolete.asset.bundle'].create({
                    'url': attachment.url,
                    'data': attachment.datas,
                    'obj_id': attachment.id,
                    'mimetype': attachment.mimetype,
                    'file_size': attachment.file_size,
                    'checksum': attachment.checksum,
                })
        return super().unlink()
