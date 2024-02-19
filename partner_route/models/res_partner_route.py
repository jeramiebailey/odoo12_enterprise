

from odoo import models, fields


class ResPartnerRoute(models.Model):
    _name = 'res.partner.route'
    _description = "Route"

    name = fields.Char(
        string='Name',
        required=True,
        translate=True
    )
