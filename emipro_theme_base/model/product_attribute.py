from odoo import api, fields, models


class product_attribute(models.Model):
    _inherit = ['product.attribute']
    
    is_quick_filter = fields.Boolean(string='Quick Filter')
  
