# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    picking_partner_id = fields.Many2one(
        store=True,
    )
