# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _order = 'default_code, name, variant_sequence, id'

    variant_sequence = fields.Char(
        string='Variant Sequence',
        compute='_compute_variant_sequence',
        store=True,
        index=True,
    )

    @api.depends('attribute_value_ids.sequence')
    def _compute_variant_sequence(self):
        for product in self:
            variable_attributes = product.attribute_line_ids.filtered(
                lambda l: len(l.value_ids) > 1).mapped('attribute_id')
            product.variant_sequence = "".join(
                ['{:05d}'.format(v.sequence) for v in
                 product.attribute_value_ids if
                 v.attribute_id in variable_attributes])
