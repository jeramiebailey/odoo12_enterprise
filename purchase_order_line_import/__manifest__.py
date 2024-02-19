# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Order Line Import',
    'summary': 'Import Purchase Order Lines.',
    'version': '12.0.1.0.0',
    'category': 'Purchase',
    'author': 'JB',
    'license': 'AGPL-3',
    'auto_install': False,
    'depends': [
        'purchase',
        'base_import_one2many',
    ],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}

