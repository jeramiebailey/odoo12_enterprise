from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pos_customer_tax_ids = fields.Many2many('account.tax', 'pos_product_customer_taxes_rel',
                                            'product_id', 'tax_id', string='POS Customer Taxes',
                                            domain=[('type_tax_use', '=', 'sale')])
    pos_supplier_tax_ids = fields.Many2many('account.tax', 'pos_product_supplier_taxes_rel',
                                            'product_id', 'tax_id', string='POS Vendor Taxes',
                                            domain=[('type_tax_use', '=', 'purchase')])
