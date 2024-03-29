
from odoo import _, api, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def action_purchase_product_sales(self):
        id = self.env.ref('purchase_order_line_product_sales.'
                           'product_sales_view')
        sales = self.order_id.origin.split(", ")
        lines = self.env['sale.order.line'].search([
                ('product_id', '=', self.product_id.id),
                ('order_id.name', 'in', sales),
                ('state', 'not in', ['cancel', 'done']),
            ],
            order='order_id DESC',
            limit=10,
        )
        return {
            'name': _('Sales'),
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'sale.order.line',
            'views': [(id.id, 'tree')],
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': "[('id','in',["+','.join(
                map(str, lines.ids))+"])]",
        }
