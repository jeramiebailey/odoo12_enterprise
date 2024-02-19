
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.tools.float_utils import float_round


class ProductProduct(models.Model):
    _inherit = 'product.product'

    sale_line_ids = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='product_id',
        string='Sale Order Lines',
    )

    missing_sale_qty = fields.Float(
        compute='_compute_missing_sale_qty',
        string='Missing',
        store=True,
    )

    @api.depends('sale_line_ids.qty_missing',
                 'sale_line_ids.state',
                 'sale_line_ids.order_active')
    def _compute_missing_sale_qty(self):
        domain = [
            ('order_active', '=', True),
            ('state', 'in', ['sale', 'done']),
            ('product_id', 'in', self.mapped('id')),
            ('qty_missing', '>', 0.0)
        ]
        order_lines = self.env['sale.order.line'].read_group(
            domain, ['product_id', 'qty_missing'], ['product_id'])
        sold_data = dict([(data['product_id'][0], data['qty_missing'])
                               for data in order_lines])
        for product in self:
            product.missing_sale_qty = float_round(sold_data.get(
                product.id, 0), precision_rounding=product.uom_id.rounding)

    @api.multi
    def action_missing_sales_popup(self):
        id = self.env.ref('product_missing_sale.product_missing_view')
        lines = self.env['sale.order.line'].search([
                ('order_active', '=', True),
                ('state', 'in', ['sale', 'done']),
                ('product_id', 'in', self.mapped('id')),
                ('qty_missing', '>', 0.0)
            ],
            order='date_planned',
        )
        return {
            'name': _('Missing Sales'),
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'sale.order.line',
            'views': [(id.id, 'tree')],
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': "[('id','in',["+','.join(
                map(str, lines.ids))+"])]",
        }

    @api.multi
    def action_missing_sales(self):
        action = self.env.ref('product_missing_sale.action_missing_sales').read()[0]
        lines = self.env['sale.order.line'].search([
                ('order_active', '=', True),
                ('state', 'in', ['sale', 'done']),
                ('product_id', 'in', self.mapped('id')),
                ('qty_missing', '>', 0.0)
            ],
        )
        action['domain'] = [('id', 'in', lines.ids)]
        return action


