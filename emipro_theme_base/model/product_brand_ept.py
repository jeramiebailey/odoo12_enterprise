from odoo import api, fields, models


class product_brand_ept(models.Model):
    _name = 'product.brand.ept'
    _inherit = ['website.published.multi.mixin']
    _order = 'name'
    _description= 'Product Brand'

    name = fields.Char('Brand Name', required=True,translate=True)
    description = fields.Text('Description', translate=True)
    website_id = fields.Many2one("website", string="Website")
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Select a partner for this brand if any.',
        ondelete='restrict'
    )
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
        'product.template',
        'product_brand_ept_id',
        string='Brand Products',
    )    
    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    brand_weight = fields.Integer(
        string='Brand Weight')
    
    #Return The product count of brand
    @api.multi
    @api.depends('product_ids')
    def _get_products_count(self):
        for brand in self:
            brand.products_count = len(brand.product_ids)
            
            
            
            
