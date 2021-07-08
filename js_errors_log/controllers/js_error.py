from typing import Any, Callable

from odoo import http
from odoo.http import request


def _coerce(value: Any, fallback: int = -1, value_class: Callable = int) -> int:
    try:
        return value_class(value)
    except (ValueError, TypeError):
        return fallback


class JsErrorController(http.Controller):
    @http.route('/js_error', type='json', auth='public')
    def js_error(self, name, message, data, width, height, client_width, client_height, pixel_ratio):
        ErrorType = request.env['js.error.type'].sudo()  # NOSONAR
        error_type_id = ErrorType.search([('name', "=", name)])
        if not error_type_id:
            error_type_id = ErrorType.create({'name': name})
        data = {
            'message': message,
            'data': data,
            'error_type_id': error_type_id.id,
            'user_id': request.env.user.id if request.env.user else False,
            'width': _coerce(width),
            'height': _coerce(height),
            'client_width': _coerce(client_width),
            'client_height': _coerce(client_height),
            'pixel_ratio': _coerce(pixel_ratio, value_class=float),
            'remote_addr': request.httprequest.remote_addr,
            'headers': str(request.httprequest.headers),
        }
        return {'success': bool(request.env['js.error'].sudo().create(data))}
