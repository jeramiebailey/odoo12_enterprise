# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class saleorder(models.Model):
    _inherit = 'sale.order'

    def action_create_purchase_order(self):
        self.ensure_one()
        # res = self.env['purchase.order'].browse(self._context.get('id', []))
        value = []
        pricelist = self.partner_id.property_product_pricelist
        partner_pricelist = self.partner_id.property_product_pricelist
        sale_order_name = ""
        po={}
        for data in self.order_line:

            if not data.product_id.type == 'product':
                continue
            print('data.product_id.qty_available > data.product_uom_qty',data.product_id.qty_available , data.product_uom_qty)
            if data.product_id.qty_available > data.product_uom_qty:
                continue
            supplier_infos = self.env['product.supplierinfo'].search([
                ('product_id', '=', data.product_id.id),
            ])
            vendor_id = False
            print('data.product_id',data.product_id.name,'supplier_infos',data.product_id.seller_ids)
            for e in data.product_id.seller_ids:
                vendor_id = e.name
            if not vendor_id:
                continue
            sale_order_name = data.order_id.name
            qty=data.product_uom_qty-data.product_id.qty_available
            if partner_pricelist:
                product_context = dict(self.env.context, partner_id=self.partner_id.id, date=self.date_order,
                                       uom=data.product_uom.id)
                final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(data.product_id,
                                                                                                              qty or 1.0,
                                                                                                              self.partner_id)

            else:
                final_price = data.product_id.standard_price

            l=[]
            if vendor_id in po:
                l=po[vendor_id]
                print('l',l)
                l.append([0, 0, {
                    'product_id': data.product_id.id,
                    'name': data.name,
                    'product_qty': qty,
                    # 'order_id': data.order_id.id,
                    'product_uom': data.product_uom.id,
                    'taxes_id': data.product_id.supplier_taxes_id.ids,
                    'date_planned': self.date_order,
                    'price_unit': final_price,
                }])
            else:
                l.append([0, 0, {
                    'product_id': data.product_id.id,
                    'name': data.name,
                    'product_qty':qty,
                    # 'order_id': data.order_id.id,
                    'product_uom': data.product_uom.id,
                    'taxes_id': data.product_id.supplier_taxes_id.ids,
                    'date_planned': self.date_order,
                    'price_unit': final_price,
                }])
                po[vendor_id]=l
        #     value.append([0, 0, {
        #         'product_id': data.product_id.id,
        #         'name': data.name,
        #         'product_qty': qty,
        #         # 'order_id': data.order_id.id,
        #         'product_uom': data.product_uom.id,
        #         'taxes_id': data.product_id.supplier_taxes_id.ids,
        #         'date_planned': self.date_order,
        #         'price_unit': final_price,
        #     }])
        # print('value',value)
        for vendor in po:
            # print(vendor)
            print('po[vendor]',po[vendor])
            val={
                'partner_id': vendor.id,
                'date_order': str(self.date_order),
                'order_line': po[vendor],
                'origin': sale_order_name,
                'partner_ref': sale_order_name
            }
            # print('val',val)
            p=self.env['purchase.order'].create(val)

            print('p',p)
