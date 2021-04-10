# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _default_note(self):
        if self.env['ir.config_parameter'].sudo().get_param(
                'sale.use_sale_note'):
            return self.env.user.company_id.sale_note

    note = fields.Text(default=_default_note)
