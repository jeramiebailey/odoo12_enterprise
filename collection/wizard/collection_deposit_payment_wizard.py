
from odoo import fields, models


class CollectionDepositPaymentWizard(models.TransientModel):
    _name = 'collection.deposit.payment.wizard'
    _description = 'Deposit Payment'

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        readonly=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    deposited = fields.Monetary(
        string='Deposit',
        currency_field='currency_id',
        required=True,
    )
    journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Journal',
        required=True,
        domain="[('use_in_collections', '=', True)]",
    )
    file = fields.Binary(
        string='Document',
        attachment=True,
    )
    filename = fields.Char()

    def _create_payment_vals(self):
        collection = self.env["collection.order"].browse(self._context.get("active_id"))
        partner = collection.user_id.partner_id
        payment_methods = self.journal_id.inbound_payment_method_ids
        return {
            'date': fields.date.today(),
            'amount': self.deposited,
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'payment_method_id': payment_methods and payment_methods[0].id or False,
            'ref': collection.name,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'document': self.file,
            'filename': self.filename,
            'partner_id': partner.id,
            'destination_account_id': collection.user_id.partner_id.property_account_payable_id.id,
            'collection_id': collection.id,
        }

    def deposit_payment(self):
        self.ensure_one()
        payment_vals = self._create_payment_vals()
        payment = self.env['account.payment'].create(payment_vals)
        return {
            'name': 'Deposit',
            'res_model': 'account.payment',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'view_id': self.env.ref("account.view_account_payment_form").id,
            'res_id': payment.id,
        }

