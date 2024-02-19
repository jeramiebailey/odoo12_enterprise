
from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    partner_zip = fields.Char(
        string='Customer Zip',
        readonly=True,
    )

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['partner_zip'] = ", partner.zip as partner_zip"
        groupby += ', partner.zip'
        return super(SaleReport, self)._query(
            with_clause, fields, groupby, from_clause
        )

