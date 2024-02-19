

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    schedule_duration = fields.Integer(
        string='Schedule Duration',
        default=14,
    )
