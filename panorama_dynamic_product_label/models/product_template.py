from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_name = fields.Char()
