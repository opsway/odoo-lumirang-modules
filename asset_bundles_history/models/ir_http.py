from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def binary_content(self, xmlid=None, model='ir.attachment', id=None, field='datas', unique=False, filename=None,
                       filename_field='name', download=False, mimetype=None,
                       default_mimetype='application/octet-stream', access_token=None):
        status, headers, content = super().binary_content(
            xmlid=xmlid, model=model, id=id, field=field, unique=unique, filename=filename,
            filename_field=filename_field, download=download, mimetype=mimetype,
            default_mimetype=default_mimetype, access_token=access_token)
        if status != 404 or id is None:
            return status, headers, content
        record = request.env['obsolete.asset.bundle'].search([('obj_id', "=", id,)])
        if not record:
            return status, headers, content
        mimetype = record.mimetype
        filehash = record.checksum
        content = record.data
        filename = record.url.split('/', 1)[-1]
        return self._binary_set_headers(200, content, filename, mimetype, unique, filehash=filehash, download=download)
