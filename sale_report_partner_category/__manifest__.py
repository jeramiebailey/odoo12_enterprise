{
    'name': 'Sale Report Partner Tags',
    'summary': 'Add partner tags to sale report. Works if only one tag '
               'is used on partner, otherwise duplicates amounts.',
    'version': '12.0.1.0.0',
    'category': 'Sale',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'sale',
    ],
    'data': [
        'report/sale_report_view.xml',
    ],
    'installable': True,
}
