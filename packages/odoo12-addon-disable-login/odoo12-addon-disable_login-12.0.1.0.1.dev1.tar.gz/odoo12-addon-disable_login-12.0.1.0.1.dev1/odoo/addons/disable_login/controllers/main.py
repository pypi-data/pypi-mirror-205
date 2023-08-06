from odoo import http
from odoo.addons.web.controllers import main
from odoo.tools.translate import _


class CustomLoginController(main.Home):
    @http.route("/web/login", type="http", auth="none")
    def web_login(self, redirect=None, **kw):
        main.ensure_db()
        http.request.params["login_success"] = False
        values = {k: v for k, v in http.request.params.items()}
        if http.request.httprequest.method == "POST":
            values["error"] = _("The Odoo login is disabled")
        response = http.request.render("web.login", values)
        response.headers["X-Frame-Options"] = "DENY"
        return response
