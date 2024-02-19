

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def write(self, values):
        if 'active' in values and not values['active']:
            for order in self:
                order.picking_ids.filtered(
                    lambda x: x.state not in ['done', 'cancel']).action_cancel()
        return super(SaleOrder, self).write(values)
