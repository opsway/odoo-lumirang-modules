from odoo import models, fields


class ObsoleteAssetBundle(models.Model):
    _name = 'obsolete.asset.bundle'
    _description = "Store outdated asset bundles"

    url = fields.Char()
    data = fields.Binary(attachment=True)
    obj_id = fields.Integer(index=True)
    file_size = fields.Integer(readonly=True)
    checksum = fields.Char("Checksum/SHA1", size=40, readonly=True)
    mimetype = fields.Char('Mime Type', readonly=True)
