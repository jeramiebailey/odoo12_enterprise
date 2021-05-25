# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_return = fields.Boolean(
        string='Is Return',
    )

    def action_view_invoice(self):
        if self.is_return:
            action = self.env.ref('account.action_invoice_out_refund')
            result = action.read()[0]
            create_bill = self.env.context.get('create_bill', False)
            result['context'] = {
                'type': 'out_refund',
                'default_purchase_id': self.id,
                'default_currency_id': self.currency_id.id,
                'default_company_id': self.company_id.id,
                'company_id': self.company_id.id
            }
            if len(self.invoice_ids) > 1 and not create_bill:
                result['domain'] = "[('id', 'in', " + str(self.invoice_ids.ids) + ")]"
            else:
                res = self.env.ref('account.invoice_form', False)
                form_view = [(res and res.id or False, 'form')]
                if 'views' in result:
                    result['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
                else:
                    result['views'] = form_view
                if not create_bill:
                    result['res_id'] = self.invoice_ids.id or False
            result['context']['default_origin'] = self.name
            result['context']['default_reference'] = self.partner_ref
            return result
        else:
            return super(PurchaseOrder, self).action_view_invoice()
