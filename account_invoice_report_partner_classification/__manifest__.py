{
    'name': 'Invoice Report Partner Classification',
    'summary': 'Add partner classification to inoice report',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'partner_classification',
    ],
    'data': [
        'report/account_invoice_report_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
