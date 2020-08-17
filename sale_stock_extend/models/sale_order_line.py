# -*- coding: utf-8 -*-

from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    missing_qty = fields.Float(string='Missing Qty', compute='_get_missing_qty',store=True)
    customer_city = fields.Char(related='order_id.partner_id.city')
    customer_state_id = fields.Many2one(comodel_name='res.country.state', store=True,
                                        related='order_id.partner_id.state_id')
    product_brand_id = fields.Many2one(comodel_name='product.brand', store=True, string='Product Branch',
                                       related='product_id.product_tmpl_id.product_brand_id')
    tag_customer_ids = fields.Many2many(comodel_name='res.partner.category', relation='partner_categ_sale_line',
                                        column1='sale_line', column2='partner_id',
                                        related='order_id.partner_id.category_id',store=True)

    @api.depends('product_uom_qty', 'qty_delivered')
    def _get_missing_qty(self):
        for rec in self:
            rec.missing_qty = rec.product_uom_qty - rec.qty_delivered


SaleOrderLine()
