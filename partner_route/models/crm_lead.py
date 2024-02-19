# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    partner_route_id = fields.Many2one(
        comodel_name='res.partner.route',
        related='partner_id.route_id',
        store=True,
        string='Partner Route'
    )
