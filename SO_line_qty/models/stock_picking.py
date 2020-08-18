from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
import datetime


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _compute_extra(self):
        for rec in self:
            rec.extra = rec.sale_avg_price - rec.list_price

    extra = fields.Float(string='Extra', compute='_compute_extra')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_qty_onhand = fields.Float(related="product_id.qty_available", string='Onhand Quantity')

    # @api.multi
    # @api.depends('product_id')
    # def _compute_qty_available(self):
    #     for rec in self:
    #         stock_move = self.env['stock.move'].search([('product_id', '=', rec.product_id.id), ('state', '!=', 'cancel')])
    #         qty_reserved = 0
    #         if stock_move:
    #             for move in stock_move:
    #                 qty_reserved = qty_reserved + move.product_uom_qty
    #             rec.qty_available = int(move.product_qty_onhand - qty_reserved)
    #         if not stock_move:
    #             rec.qty_available = rec.product_qty_onhand

    qty_available = fields.Float('Quantity Available', related='product_id.virtual_available')


class ProductMargin(models.TransientModel):
    _inherit = 'product.margin'

    @api.multi
    def action_open_window(self):
        self.ensure_one()
        context = dict(self.env.context or {})

        def ref(module, xml_id):
            proxy = self.env['ir.model.data']
            return proxy.get_object_reference(module, xml_id)

        model, search_view_id = ref('product', 'product_search_form_view')
        model, graph_view_id = ref('product_margin', 'view_product_margin_graph')
        model, form_view_id = ref('product_margin', 'view_product_margin_form')
        model, tree_view_id = ref('product_margin', 'view_product_margin_tree')

        context.update(invoice_state=self.invoice_state)

        if self.from_date:
            context.update(date_from=self.from_date)

        if self.to_date:
            context.update(date_to=self.to_date)

        views = [
            (tree_view_id, 'tree'),
            (form_view_id, 'form'),
            (graph_view_id, 'graph')
        ]

        from_date = datetime.datetime.combine(self.from_date, datetime.time(0, 0, 0))
        to_date = datetime.datetime.combine(self.to_date, datetime.time(0, 0, 0))

        products = []
        moves = self.env['stock.move'].search([('date', '>=', from_date), ('date', '<=', to_date)])
        for rec in moves:
            products.append(rec.product_id.id)


        return {
            'name': _('Product Margins'),
            'context': context,
            'view_type': 'form',
            "view_mode": 'tree,form,graph',
            'res_model': 'product.product',
            'type': 'ir.actions.act_window',
            'views': views,
            'view_id': False,
            'search_view_id': search_view_id,
            'domain': [('id', 'in', products)],

        }
