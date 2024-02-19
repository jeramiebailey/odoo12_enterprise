
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    county_id = fields.Many2one(
        comodel_name='res.country.state.county',
        string='County'
    )

    @api.onchange('country_id')
    def _onchange_country(self):
        if self.country_id and self.country_id != self.state_id.country_id:
            self.state_id = False
            self.county_id = False

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id and self.state_id != self.county_id.state_id:
            self.county_id = False

    @api.onchange('county_id')
    def _onchange_county(self):
        if self.county_id.state_id:
            self.state_id = self.county_id.state_id
