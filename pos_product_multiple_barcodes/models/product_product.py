
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    barcode_ids_str = fields.Text(
        string='Barcodes as string',
        compute='_compute_barcodes',
        store=True,
    )

    @api.multi
    @api.depends('barcode_ids.name')
    def _compute_barcodes(self):
        for product in self:
            product.barcode_ids_str = ','.join(
                product.mapped('barcode_ids.name'))
