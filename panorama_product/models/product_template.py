# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ejuice_ml = fields.Integer(
        string='E-juice ML',
        help='Put total ML of E-juice products. Used for tax calculation.'
    )
