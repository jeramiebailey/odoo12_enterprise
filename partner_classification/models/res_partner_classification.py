from odoo import models, fields


class ResPartnerClassification(models.Model):
    _name = 'res.partner.classification'
    _description = "Classification"

    name = fields.Char(required=True, translate=True)
