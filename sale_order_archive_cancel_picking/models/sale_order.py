# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def write(self, values):
        if 'active' in values and not values['active']:
            for order in self:
                order.picking_ids.filtered(
                    lambda x: x.state not in ['done', 'cancel']).action_cancel()
        return super(SaleOrder, self).write(values)
