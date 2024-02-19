
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def recalculate_prices(self):
        for line in self.mapped('order_line'):
            dict = line._convert_to_write(line.read()[0])
            line2 = self.env['purchase.order.line'].new(dict)
            line2._onchange_quantity()
            line.write({
                'price_unit': line2.price_unit,
            })
        return True
