from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        company = self.company_id or self.env.user.company_id
        v_comment = company.with_context(lang=self.partner_id.lang).sale_note or (
                    self._origin.company_id == company and self.comment)
        self.write({'comment': v_comment})
        comment_chk = self.env['account.invoice'].sudo().search([('comment', 'like', '')])
        for line in comment_chk:
            line.write({'comment': v_comment})
        return res

AccountInvoice()