from odoo import models,fields

class shopify_payment_gateway(models.Model):
    _name = 'shopify.payment.gateway'
    _description = "Shopify Payment Gateway"
    
    name = fields.Char("Name",help="Payment method name")
    code = fields.Char("Code",help="Payment method code given by Shopify")
    shopify_instance_id=fields.Many2one("shopify.instance.ept",required=True,string="Instance")