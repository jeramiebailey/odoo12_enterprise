{
    'name': 'Purchase Order From Remaining',
    'summary': 'Create backorders from purchase remaining quantities',
    'version': '12.0.1.0.0',
    'category': 'Purchase',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'purchase_stock',
    ],
    'data': [
        'wizard/purchase_order_from_remaining_qty.xml',
        'views/purchase_order_view.xml',
    ],
    'installable': True,
}
