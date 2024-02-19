{
    'name': 'Sale Order Incoming Purchases',
    'summary': 'Adds Incoming Purchases for Missing Products on Sale Orders',
    'version': '12.0.1.0.0',
    'category': 'Sale',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'product_incoming_purchase',
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
}
