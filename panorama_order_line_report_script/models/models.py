# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def create_report_line(self):
        report_line = self.env['sale.purchase.order.line']
        for rec in self:
            report_line.create({
                'sale_order_line_id': rec.id,
                'product_id': rec.product_id.id,
                'product_uom_qty': rec.product_uom_qty,
                'price_unit': rec.price_unit,
                'ref_order': rec.order_id.name,
                'qty_delivered': rec.qty_delivered,
                'missing_qty': rec.missing_qty,
                'qty_invoiced': rec.qty_invoiced,
                'price_subtotal': rec.price_subtotal,
                'date_order': rec.order_id.confirmation_date
            })


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def create_report_line(self):
        report_line = self.env['sale.purchase.order.line']
        for rec in self:
            report_line.create({
                'purchase_order_line_id': rec.id,
                'product_id': rec.product_id.id,
                'product_qty': rec.product_qty,
                'price_unit': rec.price_unit,
                'ref_order': rec.order_id.name,
                'received_qty': rec.qty_received,
                'billed_qty': rec.qty_invoiced,
                'price_subtotal': rec.price_subtotal,
                'date_order': rec.order_id.date_order

            })
