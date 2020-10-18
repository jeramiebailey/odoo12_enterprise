# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.website.controllers.main import QueryURL

from odoo import http
from odoo.http import request

class ThemeSyncoria(http.Controller):

    @http.route('/syncoria_theme/google_maps_api_key', type='json', auth='public', website=True)
    def google_maps_api_key(self):
        return json.dumps({
            'google_maps_api_key': request.website.google_maps_api_key or ''
        })

    @http.route('/syncoria/category/<int:category>', auth='public', website=True)
    def snippet_category(self, category=0, **post):
        if not category:
            raise NotFound()
        keep = QueryURL('/shop', category=category)
        return request.render('theme_syncoria_electronics.snippet_seller_template', {'category_id': category, 'keep': keep})

    @http.route('/syncoria/product_lists', auth='public', website=True)
    def snippet_productlist(self, **data):
        product_lists = request.env['syncoria.product.list'].browse([int(plist) for plist in data.get('productLists','').split(',')])
        unique_id = data.get('id')
        keep = QueryURL('/shop', category=0)
        return request.render('theme_syncoria_electronics.snippet_productlist_block', {'product_lists': product_lists, 'id': unique_id, 'keep':keep})
    
    @http.route('/syncoria/top_product_list', auth='public', website=True)
    def snippet_topfeatures(self, **data):
        product_list = request.env['syncoria.product.list'].browse(int(data.get('productList','1')))
        return request.render('theme_syncoria_electronics.snippet_topfeatures_block', {'product_list': product_list})
    
    @http.route('/syncoria/dealweeks', auth='public', website=True)
    def snippet_dealweeks(self, **data):
        product_list = request.env['syncoria.product.list'].browse(int(data.get('productList','1')))
        return request.render('theme_syncoria_electronics.snippet_dealweek_block', {'product_list': product_list})

    @http.route(['/shop/change_shop_view/<view_type>'], type='http', auth="public", website=True, sitemap=False)
    def view_change(self, view_type, **post):
        if view_type in ('custom-switch-view-list','custom-switch-view-grid'):
            request.session['shop_view'] = view_type
            return json.dumps({'success': True})
        else:
            return json.dumps({'success': False})