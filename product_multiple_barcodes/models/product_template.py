# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    barcode_ids = fields.One2many(related='product_variant_ids.barcode_ids', readonly=False)

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        barcode = False
        for arg in args:
            if arg[0] == 'barcode':
                barcode = arg[2]
                operator = arg[1]
        if barcode and operator:
            args = ['|', ('barcode_ids.name', operator, barcode)] + args
        return super(ProductTemplate, self)._search(
            args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
