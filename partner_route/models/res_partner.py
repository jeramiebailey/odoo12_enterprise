

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    route_id = fields.Many2one(
        comodel_name='res.partner.route',
        string='Route'
    )
