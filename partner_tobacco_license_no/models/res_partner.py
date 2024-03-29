# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tobacco_license_number = fields.Char(
        string='Tobacco License Number',
        compute=lambda s: s._compute_identification(
            'tobacco_license_number', 'tln',
        ),
        inverse=lambda s: s._inverse_identification(
            'tobacco_license_number', 'tln',
        ),
        search=lambda s, *a: s._search_identification(
            'tln', *a
        ),
    )

    tobacco_license_validity_date = fields.Date(
        string='Tobacco License Validity Date',
    )
