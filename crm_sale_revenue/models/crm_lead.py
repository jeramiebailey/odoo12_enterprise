# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sale_total_amount = fields.Monetary(
        compute='_compute_sale_total_amount',
        store=True,
        string="Sum of Orders",
        help="Untaxed Total Amount of Confirmed Orders",
        currency_field='company_currency'
    )

    @api.depends('order_ids.amount_untaxed', 'order_ids.state')
    def _compute_sale_total_amount(self):
        for lead in self:
            total = 0.0
            company_currency = lead.company_currency or self.env.user.company_id.currency_id
            for order in lead.order_ids:
                if order.state not in ('draft', 'sent', 'cancel'):
                    total += order.currency_id._convert(
                        order.amount_untaxed, company_currency, order.company_id,
                        order.date_order or fields.Date.today())
            lead.sale_total_amount = total
