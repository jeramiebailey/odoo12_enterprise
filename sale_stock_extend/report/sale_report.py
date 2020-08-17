from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    missing_qty = fields.Float('Qty Missing', readonly=True, digits=(1, 3), default=0.000)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['missing_qty'] = ", sum(l.missing_qty / u.factor * u2.factor) as missing_qty"
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)


SaleReport()
