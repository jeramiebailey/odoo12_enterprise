# -*- coding: utf-8 -*-
from odoo import models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_product_multiline_description_sale(self):
        name = self.display_name
        return name
