# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.tools.float_utils import float_round


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    order_active = fields.Boolean(
        string='Order Active',
        related='order_id.active',
        store=True,
    )

    qty_missing = fields.Float(
        string='Missing Qty',
        compute='_compute_missing_qty',
        store=True,
    )

    @api.depends('order_active', 'product_uom_qty', 'qty_delivered')
    def _compute_missing_qty(self):
        for rec in self:
            if rec.order_active and rec.product_uom_qty > rec.qty_delivered:
                rec.qty_missing = rec.product_uom_qty - rec.qty_delivered
            else:
                rec.qty_missing = 0
