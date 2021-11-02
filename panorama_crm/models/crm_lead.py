# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    order_ids = fields.One2many(
        domain=['|', ('active', '=', False), ('active', '=', True)]
    )
