# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_route = fields.Many2one(
        comodel_name='res.partner.route',
        related='partner_id.route_id',
        store=True,
        string='Partner Route'
    )
