# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    partner_category_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Partner Tag',
        readonly=True,
    )

    def _select(self):
        res = super()._select()
        res += """
            ,sub.partner_category_id as partner_category_id
            """
        return res

    def _sub_select(self):
        res = super()._sub_select()
        res += """
            ,pc.category_id as partner_category_id
            """
        return res

    def _from(self):
        res = super(AccountInvoiceReport, self)._from()
        res += """
                left join res_partner_res_partner_category_rel pc on (partner.id = pc.partner_id)
              """
        return res

    def _group_by(self):
        res = super()._group_by()
        res += ",pc.category_id"
        return res
