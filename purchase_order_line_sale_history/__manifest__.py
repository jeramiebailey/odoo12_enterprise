
{
    'name': 'Purchase Order Line Sale History',
    'summary': 'Purchase order line sale history',
    'version': '12.0.1.0.0',
    'category': 'Purchase',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
        'sale',
    ],
    'data': [
        'wizards/purchase_order_line_sale_history.xml',
        "views/purchase_views.xml",
    ],
    'installable': True,
    'auto_install': False,
}
