from odoo import api, fields, models
from odoo.tools.translate import html_translate

class website_menu(models.Model):
    _inherit = "website.menu"
    
    html_menu = fields.Html('Menu Design Block',translate=html_translate)
    is_dynamic_menu = fields.Boolean("Is Dynamic Menu",default=False)
    is_vertical_menu = fields.Boolean("Vertical menu",default=False)
    
    # method whcih redirect to frontend for design menu html structure
    def action_edit_menu(self, context=None):
        if not len(self.ids) == 1:
            raise ValueError('One and only one ID allowed for this action')

        url = '/menu_html_builder?model=website.menu&id=%d&enable_editor=1' % (self.id)
        return {
            'name': ('Edit Template'),
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }

    @api.onchange('is_vertical_menu')
    def is_vertical_menu_change(self):
        res=self.env['website.menu'].sudo().search([('is_vertical_menu','=',True),('website_id', 'in', (False,self.website_id.id))])
        if res:
            if self.is_vertical_menu:
                res.write({'is_vertical_menu':False})
                self.is_vertical_menu=True
            else:
                self.is_vertical_menu=False
     
    @api.one
    def _compute_visible(self):
        visible = True
        if self.page_id and not self.page_id.sudo().is_visible and not self.user_has_groups('base.group_user'):
            visible = False
        if self.is_vertical_menu:
            visible = False
        self.is_visible = visible


