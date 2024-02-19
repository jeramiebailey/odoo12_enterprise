# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Account Invoice Report County',
    'summary': 'Add partner county to the account invoice report',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'base_county',
    ],
    'data': [
        'report/account_invoice_report_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
