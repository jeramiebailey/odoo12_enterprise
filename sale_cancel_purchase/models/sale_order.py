
from odoo import _, api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_cancel(self):
        purchases = self.env['purchase.order']
        for sale_order in self:
            for sale_line in sale_order.order_line:
                for move in sale_line.move_ids:
                    purchase_line = move.created_purchase_line_id
                    if purchase_line and \
                            purchase_line.state not in \
                            ('done', 'cancel') and \
                            move.state not in \
                            ('done', 'cancel'):
                        # decrement quantities
                        sale_qty = sale_line.product_qty
                        purchase_qty = purchase_line.product_qty
                        purchase_line.product_qty = 0 \
                            if sale_qty >= purchase_qty \
                            else purchase_qty - sale_qty
                        purchases |= purchase_line.order_id
        result = super(SaleOrder, self).action_cancel()
        for purchase in purchases:
            if sum(purchase.order_line.mapped('product_uom_qty')) == 0.0:
                purchase.button_cancel()
                purchase.message_post(body=_(
                    'Purchase is cancelled automatically'))
        return result