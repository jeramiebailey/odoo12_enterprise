# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _order = 'default_code, name, variant_name, id'

    variant_name = fields.Char(
        string='Variant Name',
        compute='_compute_variant_name',
        store=True,
    )

    @api.depends('attribute_value_ids.name')
    def _compute_variant_name(self):
        for product in self:
            variable_attributes = product.attribute_line_ids.filtered(
                lambda l: len(l.value_ids) > 1).mapped('attribute_id')
            product.variant_name = product.attribute_value_ids._variant_name(
                variable_attributes)
