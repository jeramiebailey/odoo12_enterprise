
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Credit Note',
    'summary': 'Create credit note from Purchase',
    'version': '12.0.1.0.0',
    'category': 'Purchase',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'views/purchase_order_views.xml',
        'views/account_invoice_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
