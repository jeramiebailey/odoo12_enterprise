# -*- coding: utf-8 -*-
{
    'name': "Panorama Order Line Report Script",
    'depends': ['base', 'sale', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}