

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def write(self, values):
        if 'active' in values and not values['active']:
            for order in self:
                order.picking_ids.filtered(
                    lambda x: x.state not in ['done', 'cancel']).action_cancel()
        return super(PurchaseOrder, self).write(values)
