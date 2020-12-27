from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    date_of_birth = fields.Date(related='partner_id.date_of_birth', string='Date of Birth')
