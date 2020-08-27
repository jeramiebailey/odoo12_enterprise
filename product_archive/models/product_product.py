
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def write(self, vals):
        for rec in self:
            if 'active' in vals:
                if vals['active'] == False:
                    rec.is_published = False
                    rec.website_published = False
                    reordering_rule = self.env['stock.warehouse.orderpoint'].search(
                        [('product_id', '=', rec.id)])
                    if reordering_rule:
                        for line in reordering_rule:
                            line.active = False
        return super(ProductProduct, self).write(vals)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def write(self, vals):
        for rec in self:
            if 'active' in vals:
                if vals['active'] == False:
                    rec.is_published = False
                    rec.website_published = False
                    reordering_rule = self.env['stock.warehouse.orderpoint'].search(
                        [('product_id.product_tmpl_id', '=', rec.id)])
                    if reordering_rule:
                        for line in reordering_rule:
                            line.active = False
        return super(ProductTemplate, self).write(vals)