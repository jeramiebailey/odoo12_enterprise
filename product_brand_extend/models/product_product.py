
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_brand_ept_id1 = fields.Many2one(
        'product.brand',
        string='Brand',
        help='Select a brand for this product'
    )

    @api.onchange('product_brand_id')
    def onchange_date_range_id(self):
        if self.product_brand_id:
            self.product_brand_ept_id1 = self.product_brand_id

