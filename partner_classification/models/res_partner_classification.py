# Copyright 2015 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResPartnerClassification(models.Model):
    _name = 'res.partner.classification'
    _description = "Classification"

    name = fields.Char(required=True, translate=True)
