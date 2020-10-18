# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
from collections import OrderedDict
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.website.controllers.main import QueryURL

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class RecentlyViewed(WebsiteSale):
    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        res = super(RecentlyViewed, self).product(product, category, search, **kwargs)
        if product:
            recently_viewed = request.session.get('recently_viewed',[])
            if product.id in recently_viewed:
                recently_viewed.remove(product.id)
            recently_viewed.insert(0,product.id)
            request.session['recently_viewed'] = recently_viewed
        return res

        