
{
    'name': 'Purchase Create Backorder',
    'summary': 'Create backorders from purchase remaining quantities',
    'version': '12.0.1.0.0',
    'category': 'Purchase',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
    ],
    'data': [
        'wizard/purchase_create_backorder.xml',
        'views/purchase_order_view.xml',
    ],
    'installable': True,
}
