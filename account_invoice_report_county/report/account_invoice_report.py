

from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    county_id = fields.Many2one(
        comodel_name='res.country.state.county',
        string='County',
        readonly=True,
    )

    def _select(self):
        res = super()._select()
        res += """
            ,sub.county_id as county_id
            """
        return res

    def _sub_select(self):
        res = super()._sub_select()
        res += """
            ,partner.county_id as county_id
            """
        return res

    def _group_by(self):
        res = super()._group_by()
        res += ",partner.county_id"
        return res
