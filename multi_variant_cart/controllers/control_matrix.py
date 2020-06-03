# -*- coding: utf-8 -*-

from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo import http
from odoo.http import request


class WebsiteSale(WebsiteSale):
    @http.route(['/shop/product/matrix'], type='http', auth="public", website=True)
    def update_cart_matrix(self, **post):
        if post.get('product_tmpl_id'):
            request.website.get_current_pricelist()
            product_tuples = [(v, [int(s) for s in k.split('_')]) for k, v in post.items() if k[0].isdigit()]
            prod_obj = request.env['product.template']
            product_tml_id = prod_obj.sudo().browse(int(post.get('product_tmpl_id')))
            for record in product_tuples:
                qty = float(record[0]) if record[0] else 0
                if qty > 0:
                    qty = record[0]
                    product_id = product_tml_id.product_variant_ids.filtered(
                        lambda m: sorted(m.attribute_value_ids.ids) == sorted(record[1]))
                    if product_id:
                        request.website.sale_get_order(force_create=1)._cart_update(product_id=int(product_id.id),
                                                                                    add_qty=float(qty))
        return request.redirect('/shop/cart')


WebsiteSale()
