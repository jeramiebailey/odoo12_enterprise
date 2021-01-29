# -*- coding: utf-8 -*-
from odoo import models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def update_order_line(self):
        order_lines = self.env['sale.order.line'].search([])
        for order_line in order_lines:
            order_line.name = order_line.product_id.get_product_multiline_description_sale()


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_product_multiline_description_sale(self):
        name = self.display_name
        return name
