# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MisCashFlowForecastLine(models.Model):

    _inherit = 'mis.cash_flow.forecast_line'

    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead'
    )
