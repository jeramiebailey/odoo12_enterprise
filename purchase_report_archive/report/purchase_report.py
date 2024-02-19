

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


