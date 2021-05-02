# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    active = fields.Boolean(
        string='Active',
        readonly=True,
    )

    def _select(self):
        res = super(PurchaseReport, self)._select()
        return res + ", s.active as active"

    def _group_by(self):
        res = super(PurchaseReport, self)._group_by()
        return res + ", s.active"


