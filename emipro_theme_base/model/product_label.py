from odoo import models, fields, api

class product_label(models.Model):
    _name="product.label" 
    _description = "Product Label"  
    
    name=fields.Char("Name",required=True,translate=True)
    
