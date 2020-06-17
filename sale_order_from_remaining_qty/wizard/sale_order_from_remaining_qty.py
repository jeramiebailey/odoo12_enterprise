# Copyright 2020 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SaleOrderFromRemainingQty(models.TransientModel):
    _name = "sale.order.from.remaining.qty"
    _description = "Create Sale Order From Remaining Quantities"

    @api.multi
    def create_order(self):
        sale_obj = self.env['sale.order']
        sale_line_obj = self.env['sale.order.line']
        orders = sale_obj.browse(self._context.get('active_ids'))
        sale_ids = []
        for order in orders:
            if order.state in ['sale', 'done']:
                new_order = order.copy()
                new_order.order_line.unlink()
                new_order.write({
                    'origin': order.name,
                })
                sale_ids.append(new_order.id)
                for line in order.order_line:
                    if line.product_uom_qty != line.qty_delivered:
                        vals = line._convert_to_write(line.read()[0])
                        for e in ['id', 'invoice_lines', 'product_qty',
                                  'qty_delivered', 'qty_delivered_manual',
                                  'qty_to_invoice', 'move_ids']:
                            vals.pop(e)
                        vals['order_id'] = new_order.id
                        vals['product_uom_qty'] = \
                            line.product_uom_qty - line.qty_delivered
                        sale_line_obj.create(vals)
        action = self.env.ref('sale.action_orders').read()[0]
        if len(sale_ids) > 1:
            action['domain'] = [('id', 'in', sale_ids)]
        elif len(sale_ids) == 1:
            action['views'] = [(
                self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = sale_ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

