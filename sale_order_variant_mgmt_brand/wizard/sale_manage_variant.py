# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleManageVariant(models.TransientModel):
    _inherit = 'sale.manage.variant'

    product_brand_id = fields.Many2one(
        comodel_name='product.brand',
        string="Brand",
    )

    @api.onchange('product_tmpl_id')
    def _onchange_product_tmpl_id(self):
        if self.product_tmpl_id:
            self.product_brand_id = self.product_tmpl_id.product_brand_id
        return super(SaleManageVariant, self)._onchange_product_tmpl_id()
