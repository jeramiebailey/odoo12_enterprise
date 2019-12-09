# Copyright 2016 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    partner_classification_id = fields.Many2one(
        comodel_name='res.partner.classification',
        string='Partner Classification',
        readonly=True,
    )

    def _select(self):
        res = super()._select()
        res += """
            ,sub.partner_classification_id as partner_classification_id
            """
        return res

    def _sub_select(self):
        res = super()._sub_select()
        res += """
            ,partner.classification_id as partner_classification_id
            """
        return res

    def _group_by(self):
        res = super()._group_by()
        res += ",partner.classification_id"
        return res
