from odoo import models,fields

class stock_pack_operation(models.Model):
    _inherit = 'stock.pack.operation'
    
    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number')