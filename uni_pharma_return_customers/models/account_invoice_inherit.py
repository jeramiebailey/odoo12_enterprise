from odoo import fields, models, api, _
import logging
LOGGER = logging.getLogger(__name__)
from odoo.exceptions import ValidationError
TYPE2REFUND = {
    'out_invoice': 'out_refund',        # Customer Invoice
    'in_invoice': 'in_refund',          # Vendor Bill
    'out_refund': 'out_invoice',        # Customer Credit Note
    'in_refund': 'in_invoice',          # Vendor Credit Note
}
class Account_invoice_Inherit_test(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('partner_id')
    def onchange_method_partner(self):
        if self.type == 'out_invoice':
            return {
                'domain': {'partner_id': [('customer', '=', True)]}
            }
        if self.type == 'in_invoice':
            return {
                'domain': {'partner_id': [('supplier', '=', True)]}
            }
    is_manual_return_out = fields.Boolean(string="Manual Return",  )
    is_manual_return_in = fields.Boolean(string="Manual Return",  )
    auto_complete_transfer_out = fields.Many2one(comodel_name="stock.picking", string="Transfer", required=False )
    auto_complete_transfer_in = fields.Many2one(comodel_name="stock.picking", string="Transfer", required=False )

    @api.onchange('auto_complete_transfer_in')
    def onchange_method_in(self):
        if self.is_manual_return_in == True:
            if self.partner_id.id == False:
                raise ValidationError(_("Must Be Select Customer"))
        lines = []
        for line in self.auto_complete_transfer_in.move_ids_without_package:
            lines.append(
                (0, 0, {
                    'category_id': line.product_id.categ_id.id,
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    # 'price_unit': line.product_id.lst_price,
                    # 'discount': line.product_id.basic_discount,
                    'account_id':line.product_id.categ_id.property_account_income_categ_id.id,
                    'quantity':line.quantity_done,
                }))
        self.invoice_line_ids = [(6,0,[])]
        LOGGER.info("self.invoice_line_ids :: %s",self.invoice_line_ids)
        self.update({
            'invoice_line_ids': lines
        })


    @api.onchange('auto_complete_transfer_out')
    def onchange_method_out(self):
        if self.is_manual_return_out == True:
            if self.partner_id.id == False:
                raise ValidationError(_("Must Be Select Customer"))
        lines = []
        for line in self.auto_complete_transfer_out.move_ids_without_package:
            lines.append(
                (0, 0, {
                    'category_id': line.product_id.categ_id.id,
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,
                    'price_unit': line.product_id.lst_price,
                    # 'discount': line.product_id.basic_discount,
                    'account_id':line.product_id.categ_id.property_account_income_categ_id.id,
                    'quantity':line.quantity_done,
                }))
        self.update({
            'invoice_line_ids': lines
        })
