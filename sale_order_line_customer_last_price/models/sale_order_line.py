# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    customer_last_price = fields.Float(
        'Last Price',
        digits=dp.get_precision('Product Price'),
        compute='_compute_customer_last_price',
    )

    @api.depends('product_id', 'order_partner_id')
    def _compute_customer_last_price(self):
        for record in self:
            line = self.search([
                ('state', 'in', ['sale', 'done']),
                ('product_id', '=', record.product_id.id),
                ('order_partner_id', '=', record.order_partner_id.id)
            ],
                order='create_date DESC',
                limit=1,
            )
            if line:
                record.customer_last_price = line.price_unit
            else:
                record.customer_last_price = 0.0

