# Copyright 2016 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    partner_classification_id = fields.Many2one(
        comodel_name='res.partner.classification',
        string='Customer Classification',
        readonly=True,
    )

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['partner_classification_id'] = \
            ", partner.classification_id as partner_classification_id"
        groupby += ', partner.classification_id'
        return super(SaleReport, self)._query(
            with_clause, fields, groupby, from_clause
        )

