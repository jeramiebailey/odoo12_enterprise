# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrderLineSaleHistory(models.TransientModel):
    _name = "purchase.order.line.sale.history"
    _description = "Purchase order line sale history"

    purchase_order_line_id = fields.Many2one(
        comodel_name='purchase.order.line',
        string='Purchase order line',
        default=lambda self: self.env.context.get("active_id"),
    )
    product_id = fields.Many2one(
        related="purchase_order_line_id.product_id",
    )
    line_ids = fields.One2many(
        comodel_name="purchase.order.line.sale.history.line",
        inverse_name="history_id",
        string="History lines",
        readonly=True,
    )
    include_quotation = fields.Boolean(
        string="Include Quotation",
        help="Include 'Quotation' lines in the purchase history",
    )

    @api.onchange("include_quotation")
    def _onchange_quotation(self):
        self.line_ids = False
        states = ["sale", "done"]
        if self.include_quotation:
            states += ["draft", "sent"]
        domain = [
            ("product_id", "=", self.product_id.id),
            ("state", "in", states),
        ]

        vals = []
        order_lines = self.env['sale.order.line'].search(domain, limit=20)
        for order_line in order_lines:
            vals.append((0, False, {
                'sale_order_line_id': order_line.id,
                'history_purchase_order_line_id': self.purchase_order_line_id,
            }))
        self.line_ids = vals


class PurchaseOrderLineSaleHistoryline(models.TransientModel):
    _name = "purchase.order.line.sale.history.line"
    _description = "Purchase order line sale history line"

    history_id = fields.Many2one(
        comodel_name="purchase.order.line.sale.history",
        string="History",
    )
    history_purchase_order_line_id = fields.Many2one(
        comodel_name='purchase.order.line',
        string="history purchase order line",
    )
    sale_order_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Sale order line',
    )
    order_id = fields.Many2one(
        related="sale_order_line_id.order_id",
    )
    partner_id = fields.Many2one(
        related="sale_order_line_id.order_id.partner_id",
    )
    sale_order_date_order = fields.Datetime(
        related="sale_order_line_id.order_id.date_order",
    )
    product_qty = fields.Float(
        related="sale_order_line_id.product_uom_qty",
    )
    price_unit = fields.Float(
        related="sale_order_line_id.price_unit",
    )

    def _prepare_purchase_order_line_vals(self):
        self.ensure_one()
        return {'price_unit': self.price_unit}

    def action_set_price(self):
        self.ensure_one()
        vals = self._prepare_purchase_order_line_vals()
        self.history_purchase_order_line_id.write(vals)
