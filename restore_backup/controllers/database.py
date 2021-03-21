import json
import os
import sys

import jinja2
import odoo
from odoo import http
from odoo.addons.web.controllers.main import DBNAME_PATTERN
from odoo.http import request
from odoo.service import db

# Copy/Paste from web/controllers/main.py
if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('odoo.addons.restore_backup', "views")

jinja_env = jinja2.Environment(loader=loader, autoescape=True)
jinja_env.filters["json"] = json.dumps


class Restore(http.Controller):
    @http.route('/web/database/restore2', type='http', auth="none", csrf=False)
    def restore2(self, name=None, backup_path=None, master_pwd=None, ):
        data = {
            'pattern': DBNAME_PATTERN,
            'insecure': odoo.tools.config.verify_admin_password('admin'),
        }
        if request.httprequest.method == 'GET':
            return jinja_env.get_template("restore.html").render(data)
        try:
            db.check_super(master_pwd)
            db.restore_db(name, backup_path, True)
            return http.local_redirect('/web/database/manager')
        except Exception as e:
            data['error'] = "Backup restore error: {}".format(e)
        return jinja_env.get_template("restore.html").render(data)
