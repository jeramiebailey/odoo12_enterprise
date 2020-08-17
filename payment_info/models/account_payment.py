# -*- coding: utf-8 -*-
from odoo import fields, models, api
import datetime
from datetime import datetime
from dateutil import relativedelta
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    payment_info = fields.Text('Payment Info',copy=False)
