from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create_pos_purchase_order(self, pos_order_values, pos_order_workflow):
        try:
            self.env['purchase.order.line'].discount
            with_discount = True
        except:
            with_discount = False
            
        order_values = {
            'notes': pos_order_values['notes'],
            'order_line': [],
            'origin': pos_order_values['name'],
            'partner_id': pos_order_values['partner_id'],
            'partner_ref': pos_order_values['partner_ref'],
        }
        for line in pos_order_values['lines']:
            order_line_values = {
                'product_id': line[2]['product_id'],
                'product_qty': line[2]['qty'],
                'price_unit': line[2]['price_unit'],
                'taxes_id': line[2]['tax_ids'],
            }
            if with_discount:
                order_line_values['discount'] = line[2]['discount']
            order_values['order_line'].append((0, 0, order_line_values))

        session = self.env['pos.session'].browse(pos_order_values['pos_session_id'])

        # Support for POS Multi Branch
        session_data = session.read(['branch_id'])
        if session_data and session_data[0].get('branch_id'):
            order_values['branch_id'] = session_data[0].get('branch_id')[0]

        order = self.create(order_values)
        if pos_order_workflow != 'purchase.quotation':
            order.button_confirm()

        picking_update_values = {}
        if pos_order_values.get('picking_date'):
            picking_update_values['min_date'] = (pos_order_values['picking_date']
                                                 + fields.Date.context_today(self)[10:])
        if pos_order_values.get('picking_address'):
            picking_update_values['partner_address_text'] = pos_order_values['picking_address']
        if pos_order_values.get('notes'):
            picking_update_values['note'] = pos_order_values['notes']
        if picking_update_values:
            order.picking_ids.write(picking_update_values)

        if pos_order_workflow == 'purchase.order.done':
            for move in order.sudo().picking_ids.mapped('move_lines'):
                move.quantity_done = move.product_uom_qty
            order.sudo().picking_ids.action_done()

        invoice_data = False
        if pos_order_workflow in ['purchase.order.done', 'purchase.order.picking.wait']:
            context = dict(self._context or {})
            context['default_journal_id'] = session.config_id.invoice_journal_id.id
            context['type'] = 'in_invoice'

            invoice_values = {'purchase_id': order.id, 'type': 'in_invoice'}
            if session_data and session_data[0].get('branch_id'):
                invoice_values['branch_id'] = session_data[0].get('branch_id')[0]

            invoice = self.env['account.invoice'].with_context(context).create(invoice_values)
            if invoice:
                invoice.sudo().action_invoice_open()
                if not invoice.date_due:
                    invoice.date_due = invoice.date_invoice

                order.partner_id.write({'name': order.partner_id.name})
                if order.partner_id.parent_id:
                    order.partner_id.parent_id.write({'name': order.partner_id.parent_id.name})
                invoice_data = invoice.read()[0]
        return {'id': order.id, 'name': order.name, 'invoice': invoice_data}


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.model
    def _prepare_add_missing_fields(self, values):
        """ Deduce missing required fields from the onchange """
        res = {}
        onchange_fields = ['name', 'price_unit', 'product_uom', 'taxes_id', 'date_planned']
        if values.get('order_id') and values.get('product_id') and any(f not in values for f in onchange_fields):
            line = self.new(values)
            line.onchange_product_id()
            for field in onchange_fields:
                if field not in values:
                    res[field] = line._fields[field].convert_to_write(line[field], line)
        return res

    @api.model
    def create(self, values):
        values.update(self._prepare_add_missing_fields(values))
        line = super(PurchaseOrderLine, self).create(values)
        return line
