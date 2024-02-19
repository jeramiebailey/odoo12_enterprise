# -*- coding: utf-8 -*-
#################################################################################
{
    "name": "License Validity Date Notes",
    "summary": "License Validity Date Notes.",
    "category": "Sales",
    "version": "1.0.0",
    "sequence": "10",
    "author": "doaa.",
    "depends": [
        'base','sale','account','partner_tobacco_license_no'
    ],
    "data": [
        'views/account_invoice_views.xml',
        'views/sale_order_view.xml',
        'views/report_sale_order.xml',
        'views/report_account_invoice.xml',
    ],
    "application": True,
    "WBS": ' ECUSA-37',
}
