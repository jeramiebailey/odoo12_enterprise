# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    to_refund = fields.Boolean(string="To Refund (update SO/PO)",
                               help='Trigger a decrease of the delivered/received'
                                    ' quantity in the associated Sale Order/Purchase Order', default=True
                               , readonly=True)
