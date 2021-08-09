# Copyright 2021 Eska Technology LLC (www.eskaweb.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _


class CollectionRegisterPaymentWizard(models.TransientModel):
    _name = 'collection.register.payment.wizard'
    _description = 'Register Payment Wizard'

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        readonly=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    received_amount = fields.Monetary(
        string='Received Amount',
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
        line_id = self.env["collection.order.line"].browse(self._context.get("active_id"))
        partner = line_id.partner_id
        payment_methods = self.journal_id.inbound_payment_method_ids
        return {
            'date': fields.date.today(),
            'amount': self.received_amount,
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'payment_method_id': payment_methods and payment_methods[0].id or False,
            'ref': line_id.collection_order_id.name,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': partner.id,
            'document': self.file,
            'filename': self.filename,
            'destination_account_id': partner.property_account_payable_id.id,
            'collector_id': line_id.collection_order_id.user_id.partner_id.id,
            'collection_line_id': line_id.id,
        }

    def collection_register_payment(self):
        self.ensure_one()
        payment_vals = self._create_payment_vals()
        payment = self.env['account.payment'].sudo().create(payment_vals)
        payment.sudo().post()
        return {
            'name': 'Payment',
            'res_model': 'account.payment',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'view_id': self.env.ref("account.view_account_payment_form").id,
            'res_id': payment.id,
        }
