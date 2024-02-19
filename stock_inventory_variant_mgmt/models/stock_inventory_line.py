# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.inventory.line'

    product_tmpl_id_stock_variant_mgmt = fields.Many2one(
        comodel_name="product.template",
        related="product_id.product_tmpl_id",
        readonly=True
    )
    product_attribute_value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        related="product_id.attribute_value_ids",
        readonly=True
    )
