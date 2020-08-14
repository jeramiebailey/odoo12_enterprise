
from odoo import _, api, fields, models
from odoo.exceptions import UserError

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    follow_up_boolean=fields.Boolean()
    assign_to_ids = fields.Many2many('res.users',string="Assign To")

    @api.multi
    def action_invoice_paid(self):
        res = super(AccountInvoice, self).action_invoice_paid()
        for invoice in self:
            print("Falssssssssssssssssssss",invoice.assign_to_ids)
            invoice.assign_to_ids = False
        return res
