
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CountryStateCounty(models.Model):
    _name = 'res.country.state.county'
    _description = "Counties"
    _order = 'state_id,name'

    name = fields.Char(
        string='Name',
        required=True
    )
    code = fields.Char(
        string='Code'
    )
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State',
        required=True
    )
