
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
