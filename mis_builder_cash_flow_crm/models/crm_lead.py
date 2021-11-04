# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.exceptions import UserError


class Lead(models.Model):
    _inherit = 'crm.lead'

    def generate_mis_report(self):
        leads = self.env['mis.cash_flow.forecast_line'].search([
                ('lead_id', 'in', self.ids)
        ])
	leads.unlink()
        for lead in self:
            if lead.date_deadline and lead.partner_id and lead.planned_revenue:
                self.env['mis.cash_flow.forecast_line'].create({
                    'lead_id': lead.id,
                    'date': lead.date_deadline,
                    'account_id': lead.partner_id.property_account_receivable_id.id,
                    'partner_id': lead.partner_id.id,
                    'name': lead.name,
                    'balance': lead.planned_revenue,
                })
