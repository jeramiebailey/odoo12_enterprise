# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"
    auto_invoice_cash = fields.Boolean(string='Auto Invoice Cash Payment')


PosConfig()
