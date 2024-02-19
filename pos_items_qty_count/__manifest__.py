# -*- coding: utf-8 -*-
{
    'name': 'POS Count Total Items and Quantity',
    'summary': "Point of Sale Count Total Items and Total Quantity",
    'description': "Point of Sale Count Total Items and Total Quantity",

    'author': 'iPredict IT Solutions Pvt. Ltd.',
    'website': 'http://ipredictitsolutions.com',
    "support": "ipredictitsolutions@gmail.com",

    'category': 'Point of Sale',
    'version': '12.0.0.1.0',
    'depends': ['point_of_sale'],

    'data': [
        'views/assets.xml',
    ],

    'qweb': [
        'static/src/xml/pos_items_qty_count.xml'
    ],

    'license': "OPL-1",
    'price': 10,
    'currency': "EUR",

    'auto_install': True,
    'installable': True,

    'images': ['static/description/banner.png'],
}
