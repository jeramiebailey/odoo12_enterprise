# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    active = fields.Boolean(
        string='Active',
        readonly=True,
    )

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['active'] = ", s.active as active"
        groupby += ', s.active'
        return super(SaleReport, self)._query(
            with_clause, fields, groupby, from_clause
        )

