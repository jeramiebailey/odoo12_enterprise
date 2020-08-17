# -*- coding: utf-8 -*-
{
    'name': 'Sale Stock Updates',
    'summary': 'Add new fields to sale order and update others in reorder rule',
    'version': '12.0.1.0.0',
    'category': 'Sale,Stock',
    'depends': [
        'sale',
        'stock',
        'sale_stock',
        'product_brand',
    ],
    'data': [
        'views/sale_order_line_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
