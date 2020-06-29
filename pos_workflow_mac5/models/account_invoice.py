from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def create(self, values):
        onchanges = {
            'purchase_order_change': ['partner_id', 'invoice_line_ids', 'purchase_id'],
        }
        for onchange_method, changed_fields in onchanges.items():
            if any(f not in values for f in changed_fields):
                invoice = self.new(values)
                getattr(invoice, onchange_method)()
                for field in changed_fields:
                    if field not in values and invoice[field]:
                        values[field] = invoice._fields[field].convert_to_write(invoice[field], invoice)
        invoice = super(AccountInvoice, self).create(values)
        return invoice

    @api.model
    def create_pos_invoice(self, pos_order_values, pos_order_workflow):
        if pos_order_workflow in ['account.invoice.supplier', 'account.invoice.supplier.open']:
            invoice_type = 'in_invoice'
        else:
            invoice_type = 'out_invoice'

        invoice_values = {
            'comment': pos_order_values['comment'],
            'date_invoice': pos_order_values['date_invoice'] or fields.Date.context_today(self),
            'invoice_line_ids': [],
            'name': pos_order_values['partner_ref'],
            'origin': pos_order_values['name'],
            'partner_id': pos_order_values['partner_id'],
            'reference': pos_order_values['partner_ref'],
            'type': invoice_type,
            'user_id': pos_order_values['user_id'],
        }
        for line in pos_order_values['lines']:
            product = self.env['product.product'].browse(line[2]['product_id'])
            invoice_values['invoice_line_ids'].append((0, 0, {
                'product_id': product.id,
                'quantity': line[2]['qty'],
                'uom_id': product.uom_po_id.id,
                'price_unit': line[2]['price_unit'],
                'discount': line[2]['discount'],
                'invoice_line_tax_ids': line[2]['tax_ids'],
            }))

        session = self.env['pos.session'].browse(pos_order_values['pos_session_id'])

        # Support for POS Multi Branch
        session_data = session.read(['branch_id'])
        if session_data and session_data[0].get('branch_id'):
            invoice_values['branch_id'] = session_data[0].get('branch_id')[0]

        context = dict(self._context or {})
        context['default_journal_id'] = session.config_id.invoice_journal_id.id
        context['type'] = invoice_type

        invoice = self.with_context(context).create(invoice_values)
        if pos_order_workflow in ['account.invoice.customer.open', 'account.invoice.supplier.open']:
            invoice.sudo().action_invoice_open()
            if not invoice.date_due:
                invoice.date_due = invoice.date_invoice
            invoice.partner_id.write({'name': invoice.partner_id.name})
            if invoice.partner_id.parent_id:
                invoice.partner_id.parent_id.write({'name': invoice.partner_id.parent_id.name})

        if invoice_type == 'out_invoice':
            invoice_action = self.env.ref('account.action_invoice_tree1')
        else:
            invoice_action = self.env.ref('account.action_invoice_tree2')
        return {'id': invoice.id, 'number': invoice.number, 'date_invoice': invoice.date_invoice,
                'action_id': invoice_action.id, 'invoice': invoice.read()[0]}


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.model
    def create(self, values):
        onchanges = {
            '_onchange_product_id': ['account_id', 'name', 'price_unit', 'uom_id', 'invoice_line_tax_ids'],
        }
        for onchange_method, changed_fields in onchanges.items():
            if any(f not in values for f in changed_fields):
                invoice_line = self.new(values)
                getattr(invoice_line, onchange_method)()
                for field in changed_fields:
                    if field not in values and invoice_line[field]:
                        values[field] = invoice_line._fields[field].convert_to_write(invoice_line[field], invoice_line)
        invoice_line = super(AccountInvoiceLine, self).create(values)
        return invoice_line
