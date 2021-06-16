# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CountryState(models.Model):
    _inherit = "res.country.state"

    county_ids = fields.One2many(
        comodel_name='res.country.state.county',
        inverse_name='state_id',
        string='Counties'
    )
