{
    'name': 'Invoice Report Partner Tags',
    'summary': 'Add partner tags to invoice report. Works if only one tag '
               'is used on partner, otherwise duplicates amounts.',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'report/account_invoice_report_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
