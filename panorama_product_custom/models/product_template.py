# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    commerce_desc = fields.Text(
        string=' E Commerce Desc',

    )
    products_list = fields.Many2many('product.product')

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # def get_product_multiline_description_sale(self):
    #     """ Compute a multiline description of this product, in the context of sales
    #             (do not use for purchases or other display reasons that don't intend to use "description_sale").
    #         It will often be used as the default description of a sale order line referencing this product.
    #     """
    #     name = self.display_name
    #     if self.commerce_desc:
    #         name += '\n' + self.commerce_desc
    #
    #     return name
