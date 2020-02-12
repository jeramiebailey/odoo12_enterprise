# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models


class PurchaseOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _prepare_backorder(self):
        return {
            'currency_id': self.currency_id.id,
            'fiscal_position_id': self.fiscal_position_id.id,
            'incoterm_id': self.fiscal_position_id.id,
            'company_id': self.company_id.id,
        }

    @api.model
    def _prepare_backorder_line(self, line):
        return {
            'name': line.name,
            'price_unit': line.price_unit,
            'quantity': line.product_uom_qty,
            'discount': line.discount,
            'uom_id': line.product_uom.id,
            'product_id': line.product_id.id,
            'sequence': line.sequence,
            'analytic_account_id': self.analytic_account_id.id,
        }
