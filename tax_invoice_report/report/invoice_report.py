from odoo import fields, models, api, _


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    amount_taxes = fields.Float(string='Total Tax', readonly=True)

    def _select(self):
        return super(AccountInvoiceReport, self)._select() \
               + ", sub.amount_taxes as amount_taxes"

    # def _sub_select(self):
    #     return super(AccountInvoiceReport, self)._sub_select() \
    #            + ",ai.amount_tax / (SELECT count(*) FROM account_invoice_line l where invoice_id = ai.id) * count(*) * invoice_type.sign AS amount_taxes"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() \
               + ",SUM(ail.price_total * invoice_type.sign_qty) - SUM(ail.price_subtotal_signed * invoice_type.sign) AS amount_taxes"
