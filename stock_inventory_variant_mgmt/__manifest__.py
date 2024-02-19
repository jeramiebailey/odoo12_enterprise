
{
    'name': 'Stock Inventory Product Variants',
    'summary': 'Manage product variants',
    'version': '12.0.1.0.0',
    'category': 'Product',
    'author': 'JB',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'web_widget_x2many_2d_matrix',
    ],
    'data': [
        'wizard/stock_manage_variant_view.xml',
        "views/stock_inventory_view.xml",
    ],
    'installable': True,
    'auto_install': False,
}
