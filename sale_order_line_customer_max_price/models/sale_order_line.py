# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    customer_max_price = fields.Float(
        'Max Price',
        digits=dp.get_precision('Product Price'),
        compute='_compute_customer_max_price',
    )

    @api.depends('product_id', 'order_partner_id')
    def _compute_customer_max_price(self):
        for record in self:
            line = self.search([
                ('state', 'in', ['sale', 'done']),
                ('product_id', '=', record.product_id.id),
                ('order_partner_id', '=', record.order_partner_id.id)
            ],
                order='price_unit DESC',
                limit=1,
            )
            if line:
                record.customer_max_price = line.price_unit
            else:
                record.customer_max_price = 0.0

