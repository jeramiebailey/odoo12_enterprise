# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleWithLogin(WebsiteSale):
    @http.route(auth="user")
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        return super(WebsiteSaleWithLogin, self).shop(page, category,
                                                      search, ppg, **post)
