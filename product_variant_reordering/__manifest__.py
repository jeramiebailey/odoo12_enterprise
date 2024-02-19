# -*- coding: utf-8 -*-

{
    'name': 'Product Variant REordering Rule',
    'version': '12.0.1.0.0',
    "category": "Inventory",
    "depends": ["stock", "product"],
    'license': 'LGPL-3',
    'data': [
        'views/stock_production_lot.xml',
    ],
    'installable': True,
    'application': False,
}
