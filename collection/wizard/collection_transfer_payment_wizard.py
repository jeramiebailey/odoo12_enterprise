# Copyright 2021 Eska Technology LLC (www.eskaweb.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _


class CollectionTransferPaymentWizard(models.TransientModel):
    _name = 'collection.transfer.payment.wizard'
    _description = 'Transfer Payment Wizard'

    collection_id = fields.Many2one(
        comodel_name='collection.order',
        string='Destination Collection',
        required=True
    )
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

    def _create_payment_vals(self):
        collection = self.env["collection.order"].browse(self._context.get("active_id"))
        payment_methods = self.journal_id.inbound_payment_method_ids
        partner = self.collection_id.user_id.partner_id
        return {
            'date': fields.date.today(),
            'amount': self.received_amount,
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'payment_method_id': payment_methods and payment_methods[0].id or False,
            'ref': self.collection_id.name,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': partner.id,
            'destination_account_id': partner.property_account_payable_id.id,
            'collector_id': self.collection_id.user_id.partner_id.id,
            'transfer_collection_id': collection.id,
        }

    def collection_transfer_payment(self):
        self.ensure_one()
        CollectionLine = self.env['collection.order.line']
        line = CollectionLine.search([
            ('partner_id', '=', self.collection_id.user_id.partner_id.id),
            ('collection_order_id', '=', self.collection_id.id)
        ], limit=1)
        if not line:
            line = CollectionLine.sudo().create({
                'partner_id': self.collection_id.user_id.partner_id.id,
                'collection_order_id': self.collection_id.id,
            })
        payment_vals = self._create_payment_vals()
        payment_vals.update({
            'collection_line_id': line.id,
        })
        payment = self.env['account.payment'].sudo().create(payment_vals)
        payment.sudo().post()
