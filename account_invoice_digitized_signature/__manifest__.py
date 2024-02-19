# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account Invoice Digitized Signature',
    'summary': 'Account invoice digitized signature',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'web_widget_digitized_signature',
    ],
    'data': [
        'report/account_invoice_report.xml',
        'views/account_invoice_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
