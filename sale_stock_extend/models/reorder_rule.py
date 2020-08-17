# -*- coding: utf-8 -*-

from odoo import api, models


class StockReorderRule(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    @api.model
    def create(self, vals):
        res = super(StockReorderRule, self).create(vals)
        res.write({'name': res.product_id.name})
        return res


StockReorderRule()
