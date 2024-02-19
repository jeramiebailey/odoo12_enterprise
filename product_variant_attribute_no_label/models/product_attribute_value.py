# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    @api.multi
    def name_get(self):
        return super(ProductAttributeValue, self.with_context(
            show_attribute=False)).name_get()
