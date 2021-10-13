# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    barcode_ids_str = fields.Text(
        string='Barcodes as string',
        compute='_compute_barcodes',
    )

    def _compute_barcodes(self):
        vals = ''
        for product in self:
            for barcode in product.barcode_ids:
                vals += barcode.name + ','
            product.barcode_ids_str = vals
