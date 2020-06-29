# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    vendor_min_price = fields.Float(
        'Min Price',
        digits=dp.get_precision('Product Price'),
        compute='_compute_vendor_min_price',
    )

    @api.depends('product_id', 'partner_id')
    def _compute_vendor_min_price(self):
        for record in self:
            line = self.search([
                ('state', 'in', ['purchase', 'done']),
                ('product_id', '=', record.product_id.id),
                ('partner_id', '=', record.partner_id.id)
            ],
                order='price_unit',
                limit=1,
            )
            if line:
                record.vendor_min_price = line.price_unit
            else:
                record.vendor_min_price = 0.0

