from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    city = fields.Char(
        string='City',
        related='partner_id.city',
        store=True
    )
    county = fields.Many2one(
        comodel_name='res.country.state.county',
        string='County',
        related='partner_id.county_id',
        store=True
    )

