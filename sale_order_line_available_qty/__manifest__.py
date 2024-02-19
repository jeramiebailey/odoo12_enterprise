{
    'name': 'Sale Order Line Available Quantity',
    'summary': 'Adds Available Product Quantity on Sale Orders Lines',
    'version': '12.0.1.0.0',
    'category': 'Sale',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'stock_available',
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
}
