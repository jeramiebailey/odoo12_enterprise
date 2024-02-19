# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class TemplateLabelWizard(models.TransientModel):
    _name = "bi.template.label.wizard"

    product_template_ids = fields.Many2many('product.template', string="Products", required="1")
    qty = fields.Integer("Quantity")

    @api.model
    def default_get(self, fields):
        rec = super(TemplateLabelWizard, self).default_get(fields)
        rec['qty'] = 1
        rec['product_template_ids'] = self.env.context.get('active_ids', False)
        return rec

    @api.multi
    def generate_label(self):
        self = self.sudo()
        for product in self.product_template_ids:
            product.product_name = product.name
            if len(product.product_name) > 39 and not self.env.context.get('no_format'):
                product.product_name = product.product_name[:36] + "..."
        return self.env.ref('panorama_dynamic_product_label.action_bi_print_barcode_template').report_action(self, {})
