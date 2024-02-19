from odoo import models, fields


class ThemeCommon(models.Model):
    _inherit = 'website'

    footer_menu_id = fields.Many2one('website.menu', string='Footer Menu')
    copyright_text = fields.Char()
    store_location = fields.Char(default='#')
    track_order = fields.Char(default='#')


class WebsiteMenu(models.Model):
    _inherit = 'website.menu'

    website_footer = fields.One2many(
        string=u'Show in Website footer',
        comodel_name='website',
        inverse_name='footer_menu_id',
    )