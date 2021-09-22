# Copyright 2018 Clonera
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PartnerBinding(models.TransientModel):
    _inherit = 'crm.partner.binding'

    action = fields.Selection(selection=[
        ('exist', 'Link to an existing customer'),
        ('create', 'Create a new customer'),
    ])
