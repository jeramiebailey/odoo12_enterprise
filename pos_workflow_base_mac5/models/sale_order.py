from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    order_uid_save=fields.Char()
    @api.model
    def create(self, values):
        onchanges = {
            'onchange_partner_id': ['pricelist_id', 'payment_term_id',
                                      'partner_invoice_id', 'partner_shipping_id'],
        }

        new_values = dict(values or {})
        if new_values.get('date_order'):
            del new_values['date_order']

        for onchange_method, changed_fields in onchanges.items():
            if any(f not in new_values for f in changed_fields):
                order = self.new(new_values)
                getattr(order, onchange_method)()
                for field in changed_fields:
                    if field not in new_values and order[field]:
                        new_values[field] = order._fields[field].convert_to_write(order[field], order)
                        values[field] = new_values[field]
        order = super(SaleOrder, self).create(values)
        return order

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        invoice_data = super(SaleOrder, self)._prepare_invoice()

        session = self.env.context.get('session', False)
        if session and session.config_id.invoice_journal_id:
            invoice_data['journal_id'] = session.config_id.invoice_journal_id.id
        return invoice_data

    @api.model
    def create_pos_sale_order(self, pos_order_values, pos_order_workflow):
        order_values = {
            'client_order_ref': pos_order_values['client_order_ref'],
            'note': pos_order_values['note'],
            'order_line': [],
            'order_uid_save':pos_order_values['uid_save'],
            'origin': pos_order_values['name'],
            'partner_id': pos_order_values['partner_id'],
            'user_id': pos_order_values['user_id'],
        }
        if pos_order_values.get('order_date'):
            order_values['date_order'] = pos_order_values.get('order_date')

        for line in pos_order_values['lines']:
            order_values['order_line'].append((0, 0, {
                'product_id': line[2]['product_id'],
                'product_uom_qty': line[2]['qty'],
                'price_unit': line[2]['price_unit'],
                'discount': line[2]['discount'],
                'tax_id': line[2]['tax_ids'],
            }))

        session = self.env['pos.session'].browse(pos_order_values['pos_session_id'])

        # Support for POS Multi Branch
       # session_data = session.read(['branch_id'])
        #if session_data and session_data[0].get('branch_id'):
            #order_values['branch_id'] = session_data[0].get('branch_id')[0]
        if not self.search([('order_uid_save','=',pos_order_values['uid_save'])]):
            order = self.create(order_values)
            if 'sale.quotation' not in pos_order_workflow:
                order.action_confirm()

            picking_update_values = {}
            if pos_order_values.get('picking_date'):
                picking_update_values['min_date'] = (pos_order_values['picking_date']
                                                     + fields.Date.context_today(self)[10:])
            if pos_order_values.get('picking_address'):
                picking_update_values['partner_address_text'] = pos_order_values['picking_address']
            if pos_order_values.get('note'):
                picking_update_values['note'] = pos_order_values['note']
            if picking_update_values:
                order.picking_ids.write(picking_update_values)

            if pos_order_workflow == 'sale.order.done':
                for move in order.sudo().picking_ids.mapped('move_lines'):
                    move.quantity_done = move.product_uom_qty
                order.sudo().picking_ids.action_done()

            invoice = False
            if pos_order_workflow in ['sale.order.done', 'sale.order.picking.wait']:
                order.with_context(session=session).action_invoice_create()
                if order.invoice_ids:
                    order.sudo().invoice_ids.action_invoice_open()
                    if not order.invoice_ids.mapped('date_due'):
                        order.invoice_ids.update({'date_due': order.invoice_ids.mapped('date_invoice')[0]})

                    order.partner_id.write({'name': order.partner_id.name})
                    if order.partner_id.parent_id:
                        order.partner_id.parent_id.write({'name': order.partner_id.parent_id.name})
                    invoice = order.invoice_ids.read()[0]
        else:
            order=self.search([('order_uid_save','=',pos_order_values['uid_save'])],limit=1)
            invoice=order.invoice_ids.read()[0]
        return {'id': order.id, 'name': order.name, 'invoice': invoice}