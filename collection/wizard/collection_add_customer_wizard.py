
from odoo import fields, models


class CollectionAddCustomerWizard(models.TransientModel):
    _name = 'collection.add.customer.wizard'
    _description = 'Add Customer'

    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Customers',
        required=True,
        domain=[('credit', '>', 0)]
    )
    order_id = fields.Many2one(
        comodel_name='collection.order',
    )

    def collection_add_customer(self):
        for partner in self.partner_ids:
            co_line = self.env['collection.order.line'].create({
                'partner_id': partner.id,
                'collection_order_id': self.order_id.id,
            })
        return co_line
