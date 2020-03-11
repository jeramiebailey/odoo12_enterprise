# -*- coding: utf-8 -*-

import base64

import werkzeug
import werkzeug.urls

from odoo import http, SUPERUSER_ID
from odoo.http import request
import time
from odoo.tools.translate import _
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale(WebsiteSale):

    @http.route(['/shop/multi_cart'], type='http', auth="public", website=True)
    def update_cart_popup(self,**post):
        cr, uid, context,pool = request.cr, request.uid, request.context,request.registry  
        if post.get('product_tmpl_id'):
        	request.website.get_current_pricelist()
        	order=request.website.sale_get_order(force_create=1)
        	prod_obj=request.env['product.template']
        	product_data=prod_obj.sudo().browse(int(post.get('product_tmpl_id')))
        	if product_data:
        		qty=0
        		for variant in product_data.product_variant_ids:
        			qty=0
        			if post.get('qty-%s'%variant.id):
        				qty=float(post.get('qty-%s'%variant.id))
        				if qty>=1:
        					request.website.sale_get_order(force_create=1)._cart_update(product_id=int(variant.id), add_qty=float(qty))

        return request.redirect('/shop/cart')
  
