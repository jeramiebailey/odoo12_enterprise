
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    virtual_available = fields.Float(
        store=True,
    )
