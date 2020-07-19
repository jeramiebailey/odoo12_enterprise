#!/usr/bin/python3
# -*- coding: utf-8 -*-
from odoo import models, fields, api


class WizardShopifyPayoutReportEpt(models.TransientModel):
    _name = "wizard.shopify.payout.report.ept"
    _description = 'shopify.wizard.payout.report.ept'

    instance_id = fields.Many2one("shopify.instance.ept", string="Instance")
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    @api.multi
    def _check_duration(self):
        """
        Use : Check Start date and End date must be Precede.
        Added by : Deval Jagad (02/06/2020)
        Task Id : 163887
        :return: True or False
        """
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                return False
        return True

    _constraints = [
        (_check_duration, 'Error!\nThe start date must be precede its end date.',
         ['start_date', 'end_date'])
    ]

    @api.multi
    def get_payout_report(self):
        """
        Use : Import Payout Reports.
        Added by : Deval Jagad (02/06/2020)
        Task Id : 163887
        :return: True
        """
        shopify_payout_obj = self.env['shopify.payout.report.ept']
        shopify_payout_obj.get_payout_report(self.start_date, self.end_date, self.instance_id)
        return True
