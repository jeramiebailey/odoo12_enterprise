
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

