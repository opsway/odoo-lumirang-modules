from odoo import http
from odoo.http import request


class JsErrorController(http.Controller):
    @http.route('/js_error', type='json', auth='public')
    def js_error(self, name, message, data):
        ErrorType = request.env['js.error.type'].sudo()  # NOSONAR
        error_type_id = ErrorType.search([('name', "=", name)])
        if not error_type_id:
            error_type_id = ErrorType.create({'name': name})
        data = {
            'message': message,
            'data': data,
            'error_type_id': error_type_id.id,
            'user_id': request.env.user.id if request.env.user else False,
        }
        return {'success': bool(request.env['js.error'].sudo().create(data))}
