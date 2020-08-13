# -*- coding: utf-8 -*-

from datetime import datetime, date
from odoo import models, api,fields, _
from dateutil.relativedelta import relativedelta


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    @api.model
    def run_product_variant_reordering_rule(self):
        ''' This method is called from a cron job. '''
        for record in self.env['product.product'].search([]):
            reordering_rule = self.search([('product_id', '=', record.id)])
            if not reordering_rule:
                reordering = self.env['stock.warehouse.orderpoint'].create({'name': record.name,
                             'product_id': record.id,
                             'product_min_qty': 0.0,
                             'product_max_qty': 0.0,
                             'qty_multiple': 0,
                              'active': 1, 
                              'warehouse_id':1,
                              'company_id': 1, 
                              'location_id': 12})
                            