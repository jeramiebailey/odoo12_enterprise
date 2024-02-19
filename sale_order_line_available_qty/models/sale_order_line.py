
from odoo import _, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_available = fields.Float(
        related='product_id.immediately_usable_qty',
        string='Available Qty',
    )
