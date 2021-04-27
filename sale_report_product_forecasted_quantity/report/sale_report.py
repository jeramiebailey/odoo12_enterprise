# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    qty_forecasted = fields.Float(
        string='Qty Forecasted',
        readonly=True,
    )

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['virtual_available'] = ", p.virtual_available as qty_forecasted"
        groupby += ', p.virtual_available'
        return super(SaleReport, self)._query(
            with_clause, fields, groupby, from_clause
        )

