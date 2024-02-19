from odoo import models,fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    origin=fields.Char(related='invoice_id.origin')