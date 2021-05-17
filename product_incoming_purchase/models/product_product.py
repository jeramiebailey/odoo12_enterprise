# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.tools.float_utils import float_round


class ProductProduct(models.Model):
    _inherit = 'product.product'

    purchase_line_ids = fields.One2many(
        comodel_name='purchase.order.line',
        inverse_name='product_id',
        string='Purchase Order Lines',
    )

    incoming_purchase_qty = fields.Float(
        compute='_compute_incoming_purchase_qty',
        string='Incoming',
        store=True,
    )

    @api.depends('purchase_line_ids.qty_remaining',
                 'purchase_line_ids.state',
                 'purchase_line_ids.active')
    def _compute_incoming_purchase_qty(self):
        domain = [
            ('active', '=', True),
            ('state', 'in', ['purchase', 'done']),
            ('product_id', 'in', self.mapped('id')),
            ('qty_remaining', '>', 0.0)
        ]
        order_lines = self.env['purchase.order.line'].read_group(
            domain, ['product_id', 'qty_remaining'], ['product_id'])
        purchased_data = dict([(data['product_id'][0], data['qty_remaining'])
                               for data in order_lines])
        for product in self:
            product.incoming_purchase_qty = float_round(purchased_data.get(
                product.id, 0), precision_rounding=product.uom_id.rounding)

    @api.multi
    def action_incoming_purchases_popup(self):
        id = self.env.ref('product_incoming_purchase.product_incoming_view')
        lines = self.env['purchase.order.line'].search([
                ('active', '=', True),
                ('state', 'in', ['purchase', 'done']),
                ('product_id', 'in', self.mapped('id')),
                ('qty_remaining', '>', 0.0)
            ],
            order='date_planned',
        )
        return {
            'name': _('Incoming Purchases'),
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'purchase.order.line',
            'views': [(id.id, 'tree')],
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': "[('id','in',["+','.join(
                map(str, lines.ids))+"])]",
        }

    @api.multi
    def action_incoming_purchases(self):
        action = self.env.ref('product_incoming_purchase.action_incoming_purchases').read()[0]
        lines = self.env['purchase.order.line'].search([
                ('active', '=', True),
                ('state', 'in', ['purchase', 'done']),
                ('product_id', 'in', self.mapped('id')),
                ('qty_remaining', '>', 0.0)
            ],
        )
        action['domain'] = [('id', 'in', lines.ids)]
        return action


