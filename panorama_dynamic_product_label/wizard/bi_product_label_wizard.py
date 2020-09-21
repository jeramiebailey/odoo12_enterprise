from odoo import api, fields, models, _


class ProductLabelWizard(models.TransientModel):
    _name = "bi.product.label.wizard"

    product_ids = fields.Many2many('product.product', string="Products", required="1")
    qty = fields.Integer("Quantity")

    @api.model
    def default_get(self, fields):
        rec = super(ProductLabelWizard, self).default_get(fields)
        rec['qty'] = 1
        rec['product_ids'] = self.env.context.get('active_ids', False)
        return rec

    @api.multi
    def generate_label(self):
        for product in self.product_ids:
            product.product_name = product.name
            if len(product.product_name) > 30 and not self.env.context.get('no_format'):
                product.product_name = product.product_name[:30] + "..."
        return self.env.ref('panorama_dynamic_product_label.action_bi_print_barcode').report_action(self, {})
