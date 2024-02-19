
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.depends('invoice_line_ids.quantity')
    def _compute_total_qty(self):
        for invoice in self:
            total = 0.0
            for line in invoice.invoice_line_ids:
                total += line.quantity
            invoice.total_qty = total

    total_qty = fields.Float(
        string='Total Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        store=True,
        readonly=True,
        compute='_compute_total_qty',
    )
