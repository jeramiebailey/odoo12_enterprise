from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

# updated by marwa osama to update note field (terms and conditions ) automaticaly when invoice created from any place pos/so related to task ECUSA-13
    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        company = self.company_id or self.env.user.company_id
        v_comment = company.with_context(lang=self.partner_id.lang).sale_note or (
                    self._origin.company_id == company and self.comment)
        comment_chk = self.env['account.invoice'].sudo().search([])
        if comment_chk:
            for line in comment_chk:
                if len(line.comment)<=2:
                    line.write({'comment': v_comment})
        return res

AccountInvoice()