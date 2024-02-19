
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def update_to_last_price(self):
        for line in self.mapped('order_line'):
            purchase_line = self.env['purchase.order.line'].search([
                ('partner_id', '=', line.partner_id.id),
                ('product_id', '=', line.product_id.id),
                ('id', '!=', line.id),
                ('state', 'in', ['purchase', 'done']),
            ], order='date_order desc', limit=1)
            if purchase_line:
                line.write({
                    'price_unit': purchase_line.price_unit,
                })
        return True
