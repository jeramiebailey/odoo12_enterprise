# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResPartnerRoute(models.Model):
    _name = 'res.partner.route'
    _description = "Route"

    name = fields.Char(
        string='Name',
        required=True,
        translate=True
    )
