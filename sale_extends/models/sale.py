# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.tools import frozendict


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def update_order_line(self):
        sale_obj = self.env['sale.order']
        dict_val = frozendict(self.env.context)
        if dict_val.get('default_order_id'):
            order_lines = sale_obj.search([('id', '=', dict_val.get('default_order_id'))]).order_line
        else:
            order_lines = self.env['sale.order.line'].search([])
        for order_line in order_lines:
            order_line.name = order_line.product_id.get_product_multiline_description_sale()


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_product_multiline_description_sale(self):
        name = self.display_name
        return name
