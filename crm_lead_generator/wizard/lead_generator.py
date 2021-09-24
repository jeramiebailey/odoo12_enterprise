# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta
from odoo import models, fields


class LeadGeneratorWizard(models.TransientModel):
    _name = 'lead.generator.wizard'

    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Customers',
        domain=[('customer', '=', True)]
    )
    final_date = fields.Date(
        string='Final Date',
    )

    def action_generate_lead(self):
        for partner in self.partner_ids:
            partner_lead = self.env['crm.lead'].search([
                ('partner_id', '=', partner.id),
                ('type', '=', 'opportunity'),
            ], order='date_deadline desc', limit=1)

            if partner_lead.date_deadline > fields.Date.today():
                date = partner_lead.date_deadline
            else:
                date = fields.Date.today()

            duration = timedelta(days=partner.schedule_duration)
            invoices = self.env['account.invoice'].search([
                ('partner_id', '=', partner.id),
                ('type', '=', 'out_invoice'),
            ], order='date_invoice desc', limit=3).mapped('amount_total')

            revenue = 0
            if invoices:
                revenue = sum(invoices)/len(invoices)
            while self.final_date >= date:
                vals = {
                    'type': 'opportunity',
                    'user_id': self.env.user.id,
                    'name': 'Sales for ' + partner.name,
                    'partner_id': partner.id,
                    'planned_revenue': revenue,
                    'probability': 75.0,
                    'date_deadline': date,
                }
                self.env['crm.lead'].create(vals)
                date += duration
