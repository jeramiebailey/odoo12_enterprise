from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import base64, urllib

class shopify_product_image_ept(models.Model):
    _name = 'shopify.product.image.ept'
    _description = 'Shopify Product Image Ept'
    _rec_name = "position"
    
    @api.constrains('position')
    def _check_position(self):
        for image in self:
            if image.position<=0:
                raise ValidationError('Postition Must be Positive')
    
    @api.one
    def set_image(self):
        for template in self:
            if template.url:          
                try:  
                    (filename, header) = urllib.request.urlretrieve(template.url)
                    with open(filename , 'rb') as f:
                        img = base64.b64encode(f.read())
                    template.url_image_id=img
                except Exception:
                    pass
    
    @api.depends('shopify_product_tmpl_id')
    def set_instance(self):
        for shopify_gallery_img in self:
            shopify_gallery_img.shopify_instance_id = shopify_gallery_img.shopify_product_tmpl_id.shopify_instance_id.id
    
    position=fields.Integer('Position')
    shopify_product_tmpl_id=fields.Many2one('shopify.product.template.ept', string='Shopify Product')
    shopify_variant_ids=fields.Many2many('shopify.product.product.ept','shopify_product_image_rel','shopify_product_image_id','shopify_variant_id','Product Variants')
    width=fields.Integer('Width',help="Width dimension of the image which is determined on upload.")
    height=fields.Integer('Height',help="Height dimension of the image which is determined on upload.")
    url = fields.Char(size=600, string='Image URL')    
    shopify_instance_id=fields.Many2one("shopify.instance.ept",string="Instance",compute=set_instance,required=True,readonly=True)
    is_image_url=fields.Boolean("Is Image Url ?",related="shopify_instance_id.is_image_url")
    image_id=fields.Binary("Image")
    url_image_id=fields.Binary("Images",compute=set_image,store=False)
    shopify_image_id=fields.Char("Shopify Image Id")
    
    _sql_constraints = [
        ('image_position_uniq_shoipfy_ept', 'unique (position,shopify_product_tmpl_id)', 'Position of the Image must be unique !')
    ]