# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    partner_city = fields.Char(
        string='Customer City',
        readonly=True,
    )

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['partner_city'] = ", partner.city as partner_city"
        groupby += ', partner.city'
        return super(SaleReport, self)._query(
            with_clause, fields, groupby, from_clause
        )

