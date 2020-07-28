from odoo import models, fields, api


class AccountInvoiceInhr(models.Model):
    _inherit = 'account.invoice'

    # updated by marwa osama to update note field (terms and conditions ) automaticaly when invoice created from any place pos/so related to task ECUSA-13
    comment = fields.Text('Additional Information', compute='defualt_comment',readonly=True, states={'draft': [('readonly', False)]})

    @api.multi
    def defualt_comment(self):
        for item in self:
            item.comment = self.env.user.company_id.sale_note
        return True


AccountInvoiceInhr()