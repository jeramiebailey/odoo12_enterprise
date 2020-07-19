from odoo import models,fields

class stock_quant_package(models.Model):    
    _inherit = 'stock.quant.package'
    
    tracking_url = fields.Char("Tracking URL")