# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.tools.float_utils import float_round


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'


    active = fields.Boolean(
        string='Active',
        related='order_id.active',
        store=True,
    )

    qty_remaining = fields.Float(
        string='Remaining Qty',
        compute='_compute_remaining_qty',
        store=True,
    )

    @api.depends('active', 'product_qty', 'qty_received')
    def _compute_remaining_qty(self):
        for rec in self:
            if rec.active and rec.product_qty > rec.qty_received:
                rec.qty_remaining = rec.product_qty - rec.qty_received
            else:
                rec.qty_remaining = 0
