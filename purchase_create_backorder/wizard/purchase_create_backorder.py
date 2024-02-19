
from odoo import _, api, fields, models


class PurchaseCreateBackorder(models.TransientModel):
    _name = "purchase.create.backorder"
    _description = "Create Contract"

    partner_id = fields.Many2one(
        string='Vendor',
        comodel_name='res.partner',
        required=True,
    )

    @api.multi
    def create_backorder(self):
        purchase_obj = self.env['purchase.order']
        purchase_line_obj = self.env['purchase.order.line']
        orders = purchase_obj.browse(self._context.get('active_ids'))
        purchase_ids = []
        for order in orders:
            if order.state in ['purchase', 'done']:
                new_order = purchase_obj.create({
                    'partner_id': self.partner_id.id,
                })
                purchase_ids.append(new_order.id)
                for line in order.order_line:
                    if line.product_uom_qty != line.qty_received:
                        vals = line._convert_to_write(line.read()[0])
                        for e in ['id', 'invoice_lines', 'move_ids',
                                  'move_dest_ids', 'orderpoint_id']:
                            vals.pop(e)
                        vals['order_id'] = new_order.id
                        vals['product_qty'] = \
                            line.product_uom_qty - line.qty_received
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

