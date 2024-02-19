
from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    origin = fields.Char(
        string='Source Document',
        readonly=True,
    )

    def _select(self):
        res = super()._select()
        res += """
            ,sub.origin
            """
        return res

    def _sub_select(self):
        res = super()._sub_select()
        res += """
            ,ai.origin as origin
            """
        return res

    def _group_by(self):
        res = super()._group_by()
        res += ",ai.origin"
        return res
