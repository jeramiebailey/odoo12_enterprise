# Copyright 2019 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sales_permit_number = fields.Char(
        string='Sales Permit Number',
        compute=lambda s: s._compute_identification(
            'sales_permit_number', 'spn',
        ),
        inverse=lambda s: s._inverse_identification(
            'sales_permit_number', 'spn',
        ),
        search=lambda s, *a: s._search_identification(
            'spn', *a
        ),
    )
