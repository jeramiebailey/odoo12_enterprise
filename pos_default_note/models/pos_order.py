

from odoo import fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _default_note(self):
        if self.env['ir.config_parameter'].sudo().get_param(
                'sale.use_sale_note'):
            return self.env.user.company_id.sale_note

    note = fields.Text(default=_default_note)
