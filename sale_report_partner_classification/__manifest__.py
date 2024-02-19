{
    'name': 'Sale Report Partner Classification',
    'summary': 'Add partner classification to sale report',
    'version': '12.0.1.0.0',
    'category': 'Sale',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'partner_classification',
    ],
    'data': [
        'report/sale_report_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
