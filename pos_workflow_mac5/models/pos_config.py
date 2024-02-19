from odoo import fields, models

POS_WORKFLOWS = [
    ('sale.quotation', 'Create Sales Quotation'),
    ('sale.order', 'Create Sales Order'),
    ('sale.order.picking.wait', 'Create Sales Order, Waiting Delivery & Posted Invoice'),
    ('sale.order.done', 'Create Sales Order, Done Delivery & Posted Invoice'),
    ('purchase.quotation', 'Create Purchase Quotation'),
    ('purchase.order', 'Create Purchase Order'),
    ('purchase.order.picking.wait', 'Create Purchase Order, Waiting Reception & Posted Invoice'),
    ('purchase.order.done', 'Create Purchase Order, Done Reception & Posted Invoice'),
    ('account.invoice.customer', 'Create Customer Invoice'),
    ('account.invoice.customer.open', 'Create Validated Customer Invoice'),
    ('account.invoice.supplier', 'Create Vendor Bill'),
    ('account.invoice.supplier.open', 'Create Validated Vendor Bill'),
]


class pos_config(models.Model):
    _inherit = 'pos.config'

    invoice_journal_id = fields.Many2one(domain=[('type', '=', ['purchase', 'sale'])])
    pos_workflow = fields.Selection(selection_add=POS_WORKFLOWS)