

from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    city = fields.Char(
        string='City',
        readonly=True,
    )

    def _select(self):
        res = super()._select()
        res += """
            ,sub.city as city
            """
        return res

    def _sub_select(self):
        res = super()._sub_select()
        res += """
            ,partner.city as city
            """
        return res

    def _group_by(self):
        res = super()._group_by()
        res += ",partner.city"
        return res
