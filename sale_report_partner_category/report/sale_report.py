# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    partner_category_id = fields.Many2one(
        comodel_name='res.partner.category',
        string='Customer Tag',
        readonly=True,
    )

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['partner_category_id'] = \
            ", pt.category_id as partner_category_id"
        groupby += ', pt.category_id'
        from_clause += ' left join res_partner_res_partner_category_rel pt on (partner.id = pt.partner_id) '
        return super(SaleReport, self)._query(
            with_clause, fields, groupby, from_clause
        )

