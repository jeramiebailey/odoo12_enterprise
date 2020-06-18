from odoo import api, fields, models


class Product(models.Model):
    _inherit = 'product.product'

    pos_sale_price_total = fields.Float(compute='_get_prices_with_tax', string='Sale Price with Tax')
    pos_cost_price_total = fields.Float(compute='_get_prices_with_tax', string='Cost Price with Tax')
    standard_price_computed = fields.Float(compute='_get_prices_with_tax', string='Cost Price (Computed)')

    @api.multi
    def _get_prices_with_tax(self):
        company = self.env.user.company_id
        currency = company.currency_id
        for product in self:
            product.pos_sale_price_total = product.pos_customer_tax_ids.compute_pos_price_total(product.list_price, currency=currency, product=product)['total_included']
            standard_price = product.standard_price
            if product.uom_id != product.uom_po_id:
                standard_price = product.uom_id._compute_price(standard_price, product.uom_po_id)
            product.pos_cost_price_total = product.pos_supplier_tax_ids.compute_pos_price_total(standard_price, currency=currency, product=product)['total_included']
            product.standard_price_computed = standard_price
