# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends('order_line.product_uom_qty',
                 'order_line.qty_received',
                 'order_line.qty_invoiced')
    def _compute_total_qty(self):
        for order in self:
            ordered = received = invoiced = 0.0
            for line in order.order_line:
                ordered += line.product_uom_qty
                invoiced += line.qty_invoiced
                received += line.qty_received
            # for picking in order.picking_ids:
            #     received += picking.total_qty_done
            order.update({
                'total_qty_ordered': ordered,
                'total_qty_received': received,
                'total_qty_invoiced': invoiced,
            })

    total_qty_ordered = fields.Float(
        string='Total Ordered Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        store=True,
        readonly=True,
        compute='_compute_total_qty',
    )

    total_qty_received = fields.Float(
        string='Total Received Quantity',
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
