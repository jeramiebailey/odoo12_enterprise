# Copyright 2016 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    product_db_id = fields.Char(string='Item ID',)

    def _select(self):
        res = super()._select()
        res += """
             ,sub.product_db_id as product_db_id
             """
        return res

    def _sub_select(self):
        res = super()._sub_select()
        res += """
             ,pt.id as product_db_id
             """
        return res

    def _group_by(self):
        res = super()._group_by()
        res += ",pt.id"
        return res

