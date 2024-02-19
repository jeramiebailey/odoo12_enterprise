from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError, ValidationError

class slider_filter(models.Model):
    _name = "slider.filter"
    _order= "sequence asc"
    _description = "Slider Filter"
        
    name = fields.Char(string="Name",required=True,translate=True)
    sequence = fields.Integer(string='Sequence')
    website_published = fields.Boolean(string='Website Publish')
    filter_id = fields.Many2one('ir.filters', 'Filter',required=True)
    slider_id = fields.Many2one('slider', string='Filter Product')
    
    # Set slider filter published and unpublished on website
    def website_publish_button(self):
        if self.website_published:
            self.write({'website_published':False})
        else:
            self.write({'website_published':True})
            
    # If selected Filter has no any product the raise the warning and remove that filter         
    @api.onchange('filter_id')
    def _onchange_filter_id(self):
        if self.filter_id: 
            domain = safe_eval(self.filter_id.domain)
            domain+=['|',('website_id', '=',None),('website_id', '=', self.slider_id.website_id.id),('website_published','=',True)] 
            product_count = self.env['product.template'].sudo().search_count(domain)
            if product_count < 1:
                self.filter_id=False
                raise UserError(_('Sorry! You can not set filter which is content zero product.'))
