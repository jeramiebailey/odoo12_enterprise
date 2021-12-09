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

    start_date = fields.Date(
        string='Start Date',
    )

    final_date = fields.Date(
        string='Final Date',
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
    )

    recreate = fields.Boolean(
        string='Recreate',
        help='If checked, the newer opportunities will be deleted and created again',
    )

    def action_generate_lead(self):
        for partner in self.partner_ids:
            partner_lead = self.env['crm.lead'].search([
                ('partner_id', '=', partner.id),
                ('type', '=', 'opportunity'),
            ], order='date_deadline desc', limit=1)
            if self.start_date:
                date = self.start_date
            elif not self.start_date and partner_lead and partner_lead.date_deadline \
                    and partner_lead.date_deadline > fields.Date.today():
                date = partner_lead.date_deadline
            else:
                date = fields.Date.today()
            if self.recreate:
                newer_leads = self.env['crm.lead'].search([
                    ('partner_id', '=', partner.id),
                    ('type', '=', 'opportunity'),
                    ('date_deadline', '>=', date),
                ])
                newer_leads.unlink()
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
                    'user_id': self.user_id.id if self.user_id else partner.user_id.id,
                    'name': 'Sales for ' + partner.name,
                    'partner_id': partner.id,
                    'planned_revenue': revenue,
                    'probability': 75.0,
                    'date_deadline': date,
                }
                lead = self.env['crm.lead'].create(vals)
                meeting_act_type = self.env['mail.activity.type'].search([('category', '=', 'meeting')], limit=1)
                self.env['mail.activity'].sudo().create({
                    'res_id': lead.id,
                    'date_deadline': lead.date_deadline,
                    'activity_type_id': meeting_act_type.id,
                    'summary': lead.name + ' (' + str(date) + ')',
                    'user_id': lead.user_id.id,
                    'res_model_id': self.env.ref('crm.model_crm_lead').id,
                })
                date += duration
