from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class slider(models.Model):
    _name = "slider"
    _description = "Slider"
    
    name = fields.Char(string='Name',required=True)
    website_id = fields.Many2one("website", string="Website",required=True)
    theme_id = fields.Many2one('ir.module.module',string="Theme",compute='_compute_theme')
    active = fields.Boolean("Active")
    slider_filter_ids = fields.One2many("slider.filter","slider_id", string="Filter")
    slider_style_id = fields.Many2one('slider.styles', string='Slider Style')
    slider_limit = fields.Integer(string='Slider Limit',default=10)
    slider_type = fields.Selection([('product', 'Product'),('category','Category')],string="Slider Type",default='product', required=True)

    # Set a theme_id based in website
    @api.depends('website_id')
    def _compute_theme(self):
        self.theme_id = self.website_id.theme_id.id
    
    # Remove a slider_style_id when website_id change    
    @api.onchange('website_id')
    def _onchange_website_id(self):
        self.slider_style_id = False
        
    # If it is product slider then slider_filter_ids is required else raise warning
    @api.multi
    def write(self, vals):
        res = super(slider,self).write(vals)
        if self.slider_type=='product' and not self.slider_filter_ids:
            raise UserError(_('Sorry! Please set product filters first'))
        else:
            return res
            
    # If it is product slider then slider_filter_ids is required else raise warning  
    @api.model
    def create(self,vals_list):
        res = super(slider, self).create(vals_list)
        if res.slider_type=='product' and not res.slider_filter_ids:
            raise UserError(_('Sorry! Please set product filters first'))
        else:
            return res
        
    # Redirecting to the preview controller
    def action_preview(self):
        url = '/slider-preview?rec_id='+str(self.id)
        return {
            'name': ('Edit Template'),
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
        
