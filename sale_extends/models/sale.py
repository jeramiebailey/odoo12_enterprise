# -*- coding: utf-8 -*-
from odoo import api, models, _
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

    @api.multi
    def recalculate_prices(self):
        for line in self.mapped('order_line'):
            dict = line._convert_to_write(line.read()[0])
            if 'product_tmpl_id' in line._fields:
                dict['product_tmpl_id'] = line.product_tmpl_id
            line2 = self.env['sale.order.line'].new(dict)
            # we make this to isolate changed values:
            line2.product_uom_change()
            line2._onchange_discount()
            line.write({
                'price_unit': line2.price_unit,
                'discount': line2.discount,
            })
        return True


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_product_multiline_description_sale(self):
        name = self.display_name
        return name
