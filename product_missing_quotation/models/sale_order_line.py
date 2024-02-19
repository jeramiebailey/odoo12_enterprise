
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.tools.float_utils import float_round


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_missing_quot = fields.Float(
        string='Missing Quotation Qty',
        compute='_compute_missing_quot_qty',
        store=True,
    )

    @api.depends('order_active', 'product_uom_qty', 'qty_delivered')
    def _compute_missing_quot_qty(self):
        for rec in self:
            if rec.order_active and rec.product_uom_qty > rec.qty_delivered:
                rec.qty_missing_quot = rec.product_uom_qty - rec.qty_delivered
            else:
                rec.qty_missing_quot = 0
