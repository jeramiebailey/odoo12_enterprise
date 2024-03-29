# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    barcode_ids = fields.One2many(
        'product.barcode.multi',
        'product_id',
        string='Additional Barcodes',
    )

    # THIS IS OVERRIDE SQL CONSTRAINTS.
    _sql_constraints = [
        ('barcode_uniq', 'check(1=1)', 'No error')
    ]

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        barcode = False
        for arg in args:
            if arg[0] == 'barcode':
                barcode = arg[2]
                operator = arg[1]
        if barcode and operator:
            args = ['|', ('barcode_ids.name', operator, barcode)] + args
        return super(ProductProduct, self)._search(
            args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)

    @api.constrains('barcode', 'barcode_ids', 'active')
    def _check_unique_barcode(self):
        for product in self:
            barcode_names = []
            if product.barcode_ids:
                barcode_names = product.mapped('barcode_ids.name')
            if product.barcode:
                barcode_names.append(product.barcode)
            if not barcode_names:
                continue
            products = self.env['product.product'].search([
                ('barcode', 'in', barcode_names),
                ('id', '!=', product.id),
                ('active', '=', True),
            ], limit=1)
            barcode_ids = self.env['product.barcode.multi'].search([
                ('name', 'in', barcode_names),
                ('product_id', '!=', product.id),
                ('product_id.active', '=', True),
            ], limit=1)
            if products or barcode_ids or len(barcode_names) != len(set(barcode_names)):
                raise UserError(
                    _('The following barcode(s) were found in other active products: {0}.'
                      '\nNote that product barcodes should not repeat themselves both in '
                      '"Barcode" field and "Additional Barcodes" field.').format(
                            ", ".join(barcode_names)
                      )
                )
