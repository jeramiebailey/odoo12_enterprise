
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Order Update To Last Price',
    'summary': 'Purchase order update to last price',
    'version': '12.0.1.0.0',
    'category': 'Purchase',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
