from odoo.addons.web.controllers.main import Home
from odoo import http
from odoo.http import request
import werkzeug

class HomeDebugExt(Home):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kwargs):
        user = request.context.get('uid')
        if 'debug' in kwargs.keys() and user:
            if user != int(request.env.ref('base.user_admin')):
                return werkzeug.utils.redirect('/web/login?error=access')
        
        return super(HomeDebugExt, self).web_client(s_action=s_action, **kwargs)