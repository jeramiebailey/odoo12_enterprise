from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    classification_id = fields.Many2one(
        comodel_name='res.partner.classification',
        string='Classification')
