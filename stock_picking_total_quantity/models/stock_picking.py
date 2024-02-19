
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.depends('move_ids_without_package.product_uom_qty',
                 'move_ids_without_package.quantity_done')
    def _compute_total_qty(self):
        for picking in self:
            initial = done = 0.0
            for line in picking.move_ids_without_package:
                initial += line.product_uom_qty
                done += line.quantity_done
            picking.update({
                'total_qty_initial': initial,
                'total_qty_done': done,
            })

    total_qty_initial = fields.Float(
        string='Total Initial Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        store=True,
        readonly=True,
        compute='_compute_total_qty',
    )

    total_qty_done = fields.Float(
        string='Total Done Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        store=True,
        readonly=True,
        compute='_compute_total_qty',
    )
