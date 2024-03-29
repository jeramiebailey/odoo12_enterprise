
from odoo import _, api, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def action_sale_product_purchases(self):
        id = self.env.ref('sale_order_line_product_purchases.'
                           'product_purchases_view')
        lines = self.env['purchase.order.line'].search([
            ('product_id', '=', self.product_id.id),
            ('order_id.origin', 'like', self.order_id.name),
            ('state', 'not in', ['cancel', 'done']),
        ],
            order='order_id DESC',
            limit=10,
        )
        return {
            'name': _('Ongoing Purchases'),
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'purchase.order.line',
            'views': [(id.id, 'tree')],
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': "[('id','in',["+','.join(
                map(str, lines.ids))+"])]",
        }
