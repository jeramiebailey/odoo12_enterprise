
from odoo import _, api, fields, models


class PurchaseOrderFromRemainingQty(models.TransientModel):
    _name = "purchase.order.from.remaining.qty"
    _description = "Create Purchase Order From Remaining Quantities"

    partner_id = fields.Many2one(
        string='Vendor',
        comodel_name='res.partner',
        required=True,
    )

    @api.multi
    def create_order(self):
        purchase_obj = self.env['purchase.order']
        purchase_line_obj = self.env['purchase.order.line']
        orders = purchase_obj.browse(self._context.get('active_ids'))
        purchase_ids = []
        for order in orders:
            if order.state in ['purchase', 'done']:
                new_order = order.copy()
                new_order.order_line.unlink()
                new_order.write({
                    'partner_id': self.partner_id.id,
                    'origin': order.name,
                })
                purchase_ids.append(new_order.id)
                for line in order.order_line:
                    if line.product_uom_qty != line.qty_received:
                        vals = line._convert_to_write(line.read()[0])
                        for e in ['id', 'invoice_lines', 'move_ids',
                                  'move_dest_ids', 'orderpoint_id',
                                  'qty_received', 'qty_invoiced',
                                  'product_uom_qty']:
                            vals.pop(e)
                        vals['order_id'] = new_order.id
                        vals['product_qty'] = \
                            line.product_qty - line.qty_received
                        purchase_line_obj.create(vals)
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        if len(purchase_ids) > 1:
            action['domain'] = [('id', 'in', purchase_ids)]
        elif len(purchase_ids) == 1:
            action['views'] = [(
                self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = purchase_ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

