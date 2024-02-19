
from odoo import api, fields, models


class PurchaseManageVariant(models.TransientModel):
    _inherit = 'purchase.manage.variant'

    product_brand_id = fields.Many2one(
        comodel_name='product.brand',
        string="Brand",
    )

    @api.onchange('product_tmpl_id')
    def _onchange_product_tmpl_id(self):
        if self.product_tmpl_id:
            self.product_brand_id = self.product_tmpl_id.product_brand_id
        return super(PurchaseManageVariant, self)._onchange_product_tmpl_id()
