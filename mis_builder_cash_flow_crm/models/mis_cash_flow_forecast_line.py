

from odoo import fields, models


class MisCashFlowForecastLine(models.Model):

    _inherit = 'mis.cash_flow.forecast_line'

    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead'
    )
