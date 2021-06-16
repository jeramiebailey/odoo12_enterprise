# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    county_id = fields.Many2one(
        comodel_name='res.country.state.county',
        string='County'
    )

    def _onchange_partner_id_values(self, partner_id):
        res = super(Lead, self)._onchange_partner_id_values(partner_id)
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            res['county_id'] = partner.county_id.id
        return res

    def _create_lead_partner_data(self, name, is_company, parent_id=False):
        res = super(Lead, self)._create_lead_partner_data(name, is_company, parent_id)
        res['county_id'] = self.county_id.id
        return res

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
