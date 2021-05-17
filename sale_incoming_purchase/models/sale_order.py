# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_incoming_purchases(self):
        action = self.env.ref('product_incoming_purchase.action_incoming_purchases').read()[0]
        product_ids = self.mapped('order_line.product_id')
        lines = self.env['purchase.order.line'].search([
                ('active', '=', True),
                ('state', 'in', ['purchase', 'done']),
                ('product_id', 'in', product_ids.ids),
                ('qty_remaining', '>', 0.0)
            ],
        )
        action['domain'] = [('id', 'in', lines.ids)]
        return action

