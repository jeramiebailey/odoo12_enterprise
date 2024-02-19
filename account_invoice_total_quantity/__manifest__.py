{
    'name': 'Invoice Total Quantity',
    'summary': 'Adds Total Quantity on Invoice',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_invoice_view.xml',
        'views/report_invoice.xml',
    ],
    'installable': True,
}
