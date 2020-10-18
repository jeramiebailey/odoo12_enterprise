from odoo import models

class ThemeSyncoriaElectronics(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_syncoria_electronics_post_copy(self, mod):
        self.disable_view('website_theme_install.customize_modal')
