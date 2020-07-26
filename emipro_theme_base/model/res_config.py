from odoo import fields, models

class res_config(models.TransientModel):
    _inherit = "res.config.settings"

    facebook_sharing = fields.Boolean(string='Facebook', related='website_id.facebook_sharing',readonly=False)
    twitter_sharing = fields.Boolean(string='Twitter', related='website_id.twitter_sharing',readonly=False)
    linkedin_sharing = fields.Boolean(string='Linkedin', related='website_id.linkedin_sharing',readonly=False)
    mail_sharing = fields.Boolean(string='Mail', related='website_id.mail_sharing',readonly=False)
    number_of_product_line = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3')
    ], string="Number of lines for product name", related='website_id.number_of_product_line',
        required=True, default='1', readonly=False, help="Number of lines to show in product name for shop.")

