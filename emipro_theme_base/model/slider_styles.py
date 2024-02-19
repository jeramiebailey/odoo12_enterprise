from odoo import api, fields, models, _

class slider_styles(models.Model):
    _name = "slider.styles"
    _description = "Slider Styles"
    
    name = fields.Char(string='Name',required=True)
    theme_id = fields.Many2one('ir.module.module',string="Theme",required=True)
    
