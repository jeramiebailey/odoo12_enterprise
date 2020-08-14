from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, MONTHLY, WEEKLY, YEARLY, rrule

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class UserAssignToWizard(models.TransientModel):
    _name = 'user.assign'

    assign_to_ids = fields.Many2many('res.users',string="Assign To",required=True)

    @api.multi
    def action_assign(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['account.invoice'].browse(active_ids):
            record.assign_to_ids = self.assign_to_ids
        return {'type': 'ir.actions.act_window_close'}
