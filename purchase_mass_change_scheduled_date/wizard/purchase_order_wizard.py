# Copyright 2021 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrderWizard(models.TransientModel):
    _name = 'purchase.scheduled.date.mass.change.wizard'
    _description = 'Mass Change Scheduled Date'

    scheduled_date = fields.Datetime(
        string='Scheduled Date',
    )

    def change_scheduled_date(self):
        order_id = self._context.get("active_id")
        order = self.env['purchase.order'].browse(order_id)
        for line in order.order_line:
            line.date_planned = self.scheduled_date
