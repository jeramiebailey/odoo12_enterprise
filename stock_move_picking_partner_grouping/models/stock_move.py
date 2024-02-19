
from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    picking_partner_id = fields.Many2one(
        store=True,
    )
