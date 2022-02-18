# Copyright 2022 Eska Yazılım ve Danışmanlık A.Ş (www.eskayazilim.com.tr)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    customer_signature = fields.Binary(
        string='Customer acceptance',
        attachment=True,
    )

    @api.model
    def create(self, values):
        res = super(AccountInvoice, self).create(values)
        if res.customer_signature:
            values = {'customer_signature': res.customer_signature}
            res._track_signature(values, 'customer_signature')
        return res

    @api.multi
    def write(self, values):
        self._track_signature(values, 'customer_signature')
        return super(AccountInvoice, self).write(values)
