
from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='Partner State',
        readonly=True,
    )

    def _select(self):
        res = super()._select()
        res += """
            ,sub.state_id as state_id
            """
        return res

    def _sub_select(self):
        res = super()._sub_select()
        res += """
            ,partner.state_id as state_id
            """
        return res

    def _group_by(self):
        res = super()._group_by()
        res += ",partner.state_id"
        return res
