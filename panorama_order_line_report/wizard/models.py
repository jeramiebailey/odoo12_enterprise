from odoo import api, fields, models, _


class SalePurchaseOrderLine(models.TransientModel):
    _name = "sale.purchase.order.line.wizard"

    product_ids = fields.Many2many(comodel_name="product.product")
    sale_ids = fields.Many2many(comodel_name="sale.order")
    purchase_ids = fields.Many2many(comodel_name="purchase.order")

    def action_generate_order_lines(self):
        for rec in self:
            sale_ids = []
            purchase_ids = []
            if not rec.product_ids and rec.sale_ids or rec.purchase_ids:
                if rec.sale_ids:
                    for sale in rec.sale_ids:
                        sale_ids += sale.order_line.ids
                    print('ids', sale_ids)
                if rec.purchase_ids:
                    for purchase in rec.purchase_ids:
                        purchase_ids += purchase.order_line.ids
                    print('purchase_ids >> ', purchase_ids)
            elif rec.product_ids and not rec.sale_ids and not rec.purchase_ids:
                sale_ids += self.env['sale.order.line'].search(
                    [('product_id', 'in', rec.product_ids.ids)]).ids
                purchase_ids += self.env['purchase.order.line'].search(
                    [('product_id', 'in', rec.product_ids.ids)]).ids
            elif rec.product_ids and rec.sale_ids or rec.purchase_ids:
                if rec.sale_ids:
                    sale_ids += self.env['sale.order.line'].search(
                        [('product_id', 'in', rec.product_ids.ids), ('order_id', 'in', rec.sale_ids.ids)]).ids
                if rec.purchase_ids:
                    purchase_ids += self.env['purchase.order.line'].search(
                        [('product_id', 'in', rec.product_ids.ids), ('order_id', 'in', rec.purchase_ids.ids)]).ids
            else:
                sale_ids += self.env['sale.order.line'].search([]).ids
                purchase_ids += self.env['purchase.order.line'].search([]).ids
                # return self.env.ref('panorama_order_line_report.order_line_report_action').read()[0]
                return {
                    'name': _('Order Line Report'),
                    'view_type': 'form',
                    "view_mode": 'tree,form',
                    'res_model': 'sale.purchase.order.line',
                    'type': 'ir.actions.act_window',
                }
            return {
                'name': _('Order Line Report'),
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'sale.purchase.order.line',
                'type': 'ir.actions.act_window',
                'domain': ['|', ('sale_order_line_id', 'in', sale_ids),
                           ('purchase_order_line_id', 'in', purchase_ids), ]
            }
