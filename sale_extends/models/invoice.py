# -*- coding: utf-8 -*-
from odoo import models, _


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    def _get_invoice_line_name_from_product(self):
        """ Returns the automatic name to give to the invoice line depending on
        the product it is linked to.
        """
        self.ensure_one()
        if not self.product_id:
            return ''
        invoice_type = self.invoice_id.type
        rslt = self.product_id.partner_ref
        if invoice_type in ('in_invoice', 'in_refund'):
            if self.product_id.description_purchase:
                rslt += '\n' + self.product_id.description_purchase
        else:
            rslt = self.product_id.get_product_multiline_description_sale()
        return rslt
