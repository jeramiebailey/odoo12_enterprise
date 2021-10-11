# Copyright 2021 Eska Technology LLC (www.eskaweb.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _, exceptions
from odoo.exceptions import UserError


class CollectionOrder(models.Model):
    _name = 'collection.order'
    _description = 'Collection Order'
    _order = "date desc, id desc"

    name = fields.Char(
        string='Display Name',
        readonly=True,
        copy=False,
        default=lambda x: _('New')
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Collector',
        required=True,
        default=lambda self: self.env.user,
        states={'close': [('readonly', True)]},
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        states={'close': [('readonly', True)]},
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.user.company_id.id
    )
    state = fields.Selection([
        ('new', 'New'),
        ('ongoing', 'Ongoing'),
        ('depositing', 'Depositing'),
        ('close', 'Closed'),
    ],
        string='Status',
        compute='_compute_states',
    )
    collection_line_ids = fields.One2many(
        comodel_name='collection.order.line',
        inverse_name='collection_order_id',
        string='Collection Lines',
        states={'close': [('readonly', True)]},
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        readonly=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    total_receivable = fields.Monetary(
        string='Total Receivable Amount',
        compute='_compute_receivable',
        currency_field='currency_id',
    )
    total_collected = fields.Monetary(
        string='Total Collected Amount',
        compute='_compute_collected',
        currency_field='currency_id',
    )
    total_deposited = fields.Monetary(
        string='Total Deposited Amount',
        compute='_compute_deposited',
        currency_field='currency_id',
    )
    total_transferred = fields.Monetary(
        string='Total Transferred Amount',
        compute='_compute_transferred',
        currency_field='currency_id',
    )
    payment_ids = fields.One2many(
        comodel_name='account.payment',
        inverse_name='collection_id',
        string='Payments',
    )
    transfer_payment_ids = fields.One2many(
        comodel_name='account.payment',
        inverse_name='transfer_collection_id',
        string='Transfer Payments',
    )
    active = fields.Boolean(
        default=True,
        string="Active",
    )

    @api.depends('collection_line_ids.receivable_amount', 'currency_id')
    def _compute_receivable(self):
        for collection in self:
            collection.total_receivable = sum(line.receivable_amount for line in collection.collection_line_ids)

    @api.depends('collection_line_ids.collected_amount', 'currency_id')
    def _compute_collected(self):
        for collection in self:
            collection.total_collected = sum(line.collected_amount for line in collection.collection_line_ids)

    @api.depends('payment_ids.amount', 'payment_ids.state', 'currency_id')
    def _compute_deposited(self):
        for collection in self:
            collection.total_deposited = sum(collection.payment_ids \
                                             .filtered(lambda x: x.state in ['draft', 'posted']).mapped('amount'))

    @api.depends('transfer_payment_ids.amount', 'currency_id')
    def _compute_transferred(self):
        for collection in self:
            collection.total_transferred = sum(collection.transfer_payment_ids.mapped('amount'))

    @api.depends('total_collected', 'total_deposited', 'collection_line_ids.payment_ids.move_line_ids.reconciled')
    def _compute_states(self):
        for rec in self:
            if rec.total_deposited > 0:
                reconcile = rec.mapped('collection_line_ids.payment_ids.move_line_ids').filtered \
                    (lambda r: not r.reconciled and r.partner_id == rec.user_id.partner_id)
                if reconcile:
                    rec.state = 'depositing'
                else:
                    rec.state = 'close'
            elif rec.total_collected > 0:
                rec.state = 'ongoing'
            else:
                rec.state = 'new'

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            name = rec.name + ' (' + rec.user_id.name + ')'
            result.append((rec.id, name))
        return result

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('collection.order') or _('New')
        return super(CollectionOrder, self).create(vals)

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state != 'new':
                raise UserError(
                    _('You can not delete collections that has payments.'))
        return super(CollectionOrder, self).unlink()

    def action_deposit(self):
        view = self.env.ref('collection.collection_deposit_payment_wizard_form')
        return {
            'name': _('Deposit Payment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'collection.deposit.payment.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
        }

    def action_transfer(self):
        view = self.env.ref('collection.collection_transfer_payment_wizard_form')
        return {
            'name': _('Transfer Payment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'collection.transfer.payment.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
        }

    def add_customers(self):
        view = self.env.ref('collection.collection_add_customer_wizard_view_form')
        return {
            'name': _('Add Customer'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'collection.add.customer.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {
                'default_order_id': self.id,
            }
        }

    def button_collected_payments(self):
        return {
            'name': _('Collected Payment'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.payment',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.mapped('collection_line_ids').mapped('payment_ids').ids)],
            'context': {
                'create': False,
            },
        }

    def button_deposited_payments(self):
        return {
            'name': _('Deposited Payment'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.payment',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.mapped('payment_ids').ids)],
            'context': {
                'create': False,
            },
        }

    def button_transferred_payments(self):
        return {
            'name': _('Transferred Payment'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.payment',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.mapped('transfer_payment_ids').ids)],
            'context': {
                'create': False,
            },
        }

    def button_reconcile(self):
        accounts = self.user_id.partner_id.property_account_receivable_id
        action_context = {
            'show_mode_selector': True,
            'partner_ids': [self.user_id.partner_id.id],
            'mode': 'customers',
            'account_ids': accounts.ids
        }
        return {
            'type': 'ir.actions.client',
            'tag': 'manual_reconciliation_view',
            'context': action_context,
        }
