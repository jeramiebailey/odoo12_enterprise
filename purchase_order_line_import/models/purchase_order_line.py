# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.model
    def create(self, values):
        if self._context.get('import_one2many'):
            required_fields = ['name', 'date_planned', 'price_unit',
                               'product_uom']
            if values.get('order_id') and values.get('product_id') and \
                    any(f not in values for f in required_fields):
                line = self.new(values)
                line.onchange_product_id()
                line_values = line._convert_to_write(line._cache)
                for field in required_fields:
                    if field not in values:
                        values[field] = line_values[field]
        return super(PurchaseOrderLine, self).create(values)
