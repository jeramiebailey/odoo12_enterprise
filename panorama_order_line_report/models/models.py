# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalePurchaseOrderLine(models.Model):
    _name = 'sale.purchase.order.line'

    ref_order = fields.Char(string='Ref.')
    sale_order_line_id = fields.Many2one('sale.order.line')
    purchase_order_line_id = fields.Many2one('purchase.order.line')
    product_id = fields.Many2one(comodel_name="product.product", string="Product")
    product_uom_qty = fields.Float(string="Sales Qty", store=True, default=0.0)
    qty_delivered = fields.Float(string="Delivered Qty", store=True, default=0.0)
    missing_qty = fields.Float(string="Missing Qty", store=True, default=0.0)
    qty_invoiced = fields.Float(string="Invoiced Qty", store=True, default=0.0)
    price_unit = fields.Float(string="Unit Price", store=False)
    product_qty = fields.Float(string="Purchase Qty", store=True, default=0.0)

    @api.multi
    @api.depends('price_unit', 'product_uom_qty', 'product_qty')
    def get_price_subtotal(self):
        print('hi')
        for rec in self:
            if rec.product_uom_qty != 0:
                rec.price_subtotal = rec.price_unit * rec.product_uom_qty
            elif rec.product_qty != 0:
                rec.price_subtotal = rec.price_unit * rec.product_qty

    price_subtotal = fields.Float(string="Subtotal", compute='get_price_subtotal', store=True)

    received_qty = fields.Float(string="Received Qty", store=True, default=0.0)
    billed_qty = fields.Float(string="Billed Qty", store=True, default=0.0)
    date_order = fields.Datetime(string="Date", required=False, )


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        OrderLine = self.env['sale.purchase.order.line']
        res = super(SaleOrderLine, self).create(vals)
        OrderLine.create({
            'sale_order_line_id': res.id,
            'product_id': res.product_id.id,
            'product_uom_qty': res.product_uom_qty,
            'price_unit': res.price_unit,
            'ref_order': res.order_id.name,
        })
        return res

    @api.multi
    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        report_line = self.env['sale.purchase.order.line'].search([('sale_order_line_id', '=', self.id)])
        #report_line.write(vals)
        return res
    
    
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            report_line = self.env['sale.purchase.order.line'].search([('sale_order_line_id', '=', line.id)])
            report_line.write({
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'price_unit': line.price_unit,
                'qty_delivered': line.qty_delivered,
                'missing_qty': line.missing_qty,
                'qty_invoiced': line.qty_invoiced,
                'date_order': line.order_id.confirmation_date,
            })


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.model
    def create(self, vals):
        OrderLine = self.env['sale.purchase.order.line']
        res = super(PurchaseOrderLine, self).create(vals)
        OrderLine.create({
            'purchase_order_line_id': res.id,
            'product_id': res.product_id.id,
            'product_qty': res.product_qty,
            'price_unit': res.price_unit,
            'ref_order': res.order_id.name,
        })
        return res

    @api.multi
    def write(self, vals):
        new_vals = {}
        res = super(PurchaseOrderLine, self).write(vals)
        report_line = self.env['sale.purchase.order.line'].search([('purchase_order_line_id', '=', self.id)])
        if vals.get('product_id'):
            new_vals['product_id'] = vals.get('product_id')
        if vals.get('product_qty'):
            new_vals['product_qty'] = vals.get('product_qty')
        if vals.get('price_unit'):
            new_vals['price_unit'] = vals.get('price_unit')
        report_line.write(new_vals)
        return res


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for line in self.order_line:
            report_line = self.env['sale.purchase.order.line'].search([('purchase_order_line_id', '=', line.id)])
            report_line.write({
                'product_id': line.product_id.id,
                'product_qty': line.product_qty,
                'price_unit': line.price_unit,
                'received_qty': line.qty_received,
                'billed_qty': line.qty_invoiced,
                'date_order': line.order_id.date_order
            })







