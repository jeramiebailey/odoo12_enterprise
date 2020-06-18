# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.product_uom_qty',
                 'order_line.qty_delivered',
                 'order_line.qty_invoiced')
    def _compute_total_qty(self):
        for order in self:
            ordered = delivered = invoiced = 0.0
            for line in order.order_line:
                ordered += line.product_uom_qty
                delivered += line.qty_delivered
                invoiced += line.qty_invoiced
            order.update({
                'total_qty_ordered': ordered,
                'total_qty_delivered': delivered,
                'total_qty_invoiced': invoiced,
            })

    total_qty_ordered = fields.Float(
        string='Total Ordered Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        store=True,
        readonly=True,
        compute='_compute_total_qty',
    )

    total_qty_delivered = fields.Float(
        string='Total Delivered Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        store=True,
        readonly=True,
        compute='_compute_total_qty',
    )

    total_qty_invoiced = fields.Float(
        string='Total Invoiced Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        store=True,
        readonly=True,
        compute='_compute_total_qty',
    )
